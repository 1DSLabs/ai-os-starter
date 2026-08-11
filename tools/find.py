#!/usr/bin/env python3
"""Find the knowledge files that best match a description.

    python3 tools/find.py "how we handle a refund request"
    python3 tools/find.py "refund" --top 3

The /load command may use this as a fallback when the index cannot do the job.
No installs required. Python 3 standard library only.
"""

import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontmatter import LabelBlockError, read  # noqa: E402
from kb import KB_DEFAULT, fail, iter_knowledge_files, resolve_kb_root  # noqa: E402

WEIGHT_TITLE = 5
WEIGHT_ALIAS = 4
WEIGHT_TAG = 3
WEIGHT_SUMMARY = 2
WEIGHT_BODY = 1
CLOSE_ENOUGH = 0.82

# Words too common to be worth matching on.
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "do", "does", "for", "from",
    "how", "i", "if", "in", "is", "it", "of", "on", "or", "our", "she", "that",
    "the", "their", "them", "they", "this", "to", "we", "what", "when", "where",
    "which", "who", "with", "you", "your",
}


def words(text):
    return [w for w in re.split(r"[^a-z0-9]+", str(text).lower()) if w]


def useful_words(text):
    return [w for w in words(text) if w not in STOPWORDS and len(w) > 1]


def as_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def score_field(query_words, field_text, weight):
    targets = words(field_text)
    if not targets:
        return 0
    total = 0
    for query_word in query_words:
        if query_word in targets:
            total += weight
            continue
        best = 0.0
        for target in targets:
            ratio = difflib.SequenceMatcher(None, query_word, target).ratio()
            if ratio > best:
                best = ratio
        if best >= CLOSE_ENOUGH:
            total += weight
    return total


def load_files(kb_root):
    entries = []
    for path in iter_knowledge_files(kb_root):
        try:
            labels = read(path)
        except LabelBlockError:
            continue
        if not labels or not labels.get("id"):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                body = handle.read()
        except OSError:
            body = ""
        entries.append(
            {
                "id": labels["id"],
                "title": labels.get("title", ""),
                "summary": labels.get("summary", ""),
                "aliases": as_list(labels.get("aliases")),
                "tags": as_list(labels.get("tags")),
                "path": os.path.relpath(path, kb_root).replace(os.sep, "/"),
                "body": body,
            }
        )
    return entries


def search(query, entries, top=5):
    query_words = useful_words(query)
    if not query_words:
        return []

    results = []
    for entry in entries:
        score = 0
        score += score_field(query_words, entry["title"], WEIGHT_TITLE)
        score += score_field(query_words, entry["id"], WEIGHT_TITLE)
        for alias in entry["aliases"]:
            score += score_field(query_words, alias, WEIGHT_ALIAS)
        for tag in entry["tags"]:
            score += score_field(query_words, tag, WEIGHT_TAG)
        score += score_field(query_words, entry["summary"], WEIGHT_SUMMARY)

        body_words = set(words(entry["body"]))
        score += sum(WEIGHT_BODY for w in query_words if w in body_words)

        if score > 0:
            results.append(
                {
                    "id": entry["id"],
                    "title": entry["title"],
                    "summary": entry["summary"],
                    "path": entry["path"],
                    "score": score,
                }
            )

    results.sort(key=lambda r: (-r["score"], r["id"]))
    return results[:top]


def main(argv):
    args = [a for a in argv[1:]]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]

    top = 5
    if "--top" in args:
        i = args.index("--top")
        try:
            top = int(args[i + 1])
            del args[i : i + 2]
        except (IndexError, ValueError):
            print('Usage: python3 tools/find.py "what you are looking for" [--top N]')
            return 2

    if not args:
        print('Usage: python3 tools/find.py "what you are looking for" [--top N]')
        print('Example: python3 tools/find.py "how we onboard a new client"')
        return 2

    query = " ".join(args)
    kb_root = resolve_kb_root(KB_DEFAULT)
    entries = load_files(kb_root)

    if not entries:
        message = "There are no knowledge files yet. Add some with /ingest or /interview."
        print(json.dumps({"query": query, "results": [], "note": message}) if as_json else message)
        return 0

    results = search(query, entries, top=top)

    if as_json:
        print(json.dumps({"query": query, "results": results}, indent=2))
        return 0

    if not results:
        print('Nothing matched "%s".' % query)
        print("Searched %d file%s." % (len(entries), "" if len(entries) == 1 else "s"))
        return 0

    for result in results:
        summary = result["summary"]
        if len(summary) > 70:
            summary = summary[:67] + "..."
        print("%-30s %s" % (result["id"], result["title"]))
        if summary:
            print("%-30s %s" % ("", summary))
        print("%-30s %s" % ("", result["path"]))
        print("")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001
        fail(exc)
