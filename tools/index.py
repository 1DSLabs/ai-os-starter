#!/usr/bin/env python3
"""Build the knowledge base index.

Writes two files inside Knowledge_Base/:

  _index.json   a map of every file's id to its path, for fast lookup
  INDEX.md      a readable table of everything you have, grouped by type

Run it after you add or change files:

    python3 tools/index.py

No installs required. Python 3 standard library only.
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontmatter import LabelBlockError, read  # noqa: E402
from kb import (  # noqa: E402
    KB_DEFAULT,
    TYPE_ORDER,
    fail,
    iter_knowledge_files,
    resolve_kb_root,
)

VERSION = "3.0.0"


def build(kb_root):
    """Return (entries_by_id, problems)."""
    entries = {}
    seen_ids = {}
    problems = []

    for path in iter_knowledge_files(kb_root):
        rel = os.path.relpath(path, kb_root).replace(os.sep, "/")
        try:
            labels = read(path)
        except LabelBlockError as exc:
            problems.append("%s: %s" % (rel, exc))
            continue

        if not labels or not labels.get("id"):
            continue

        entry_id = labels["id"]
        if entry_id in seen_ids:
            problems.append(
                "two files share the id '%s': %s and %s"
                % (entry_id, seen_ids[entry_id], rel)
            )
            continue

        seen_ids[entry_id] = rel
        entries[entry_id] = {"path": rel, "labels": labels}

    return entries, problems


def _cell(value):
    """Make a value safe to drop into a markdown table cell."""
    text = " ".join(str(value).split())
    return text.replace("|", "\\|")


def write_index(kb_root, entries):
    by_type = {}
    for entry_id, entry in entries.items():
        file_type = entry["labels"].get("type") or "other"
        by_type.setdefault(file_type, []).append(entry_id)

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# What's in this brain",
        "",
        "Every file you've saved, grouped by kind. Claude reads this to find things fast.",
        "",
        "Rebuild it any time with `python3 tools/index.py`.",
        "",
        "- Files: %d" % len(entries),
        "- Updated: %s" % generated,
        "",
    ]

    if not entries:
        lines += [
            "## Nothing here yet",
            "",
            "Drop your documents into `_inbox/` and run `/ingest` in Claude Code,",
            "or run `/interview` to build your first files by answering questions.",
            "",
        ]

    known = [t for t in TYPE_ORDER if t in by_type]
    extra = sorted(t for t in by_type if t not in TYPE_ORDER)

    for file_type in known + extra:
        lines.append("## %s" % file_type.replace("_", " ").replace("-", " ").title())
        lines.append("")
        lines.append("| Name | What it covers | Owner | Updated |")
        lines.append("|---|---|---|---|")
        for entry_id in sorted(by_type[file_type]):
            labels = entries[entry_id]["labels"]
            path = entries[entry_id]["path"]
            lines.append(
                "| [%s](%s) | %s | %s | %s |"
                % (
                    _cell(labels.get("title") or entry_id),
                    path,
                    _cell(labels.get("summary", "")),
                    _cell(labels.get("owner", "")),
                    _cell(labels.get("updated", "")),
                )
            )
        lines.append("")

    with open(os.path.join(kb_root, "INDEX.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def write_map(kb_root, entries):
    payload = {
        "version": VERSION,
        "generated": datetime.now(timezone.utc).isoformat(),
        "files": {k: v["path"] for k, v in sorted(entries.items())},
    }
    with open(os.path.join(kb_root, "_index.json"), "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def main(argv):
    kb_root = resolve_kb_root(argv[1] if len(argv) > 1 else KB_DEFAULT)
    entries, problems = build(kb_root)

    write_map(kb_root, entries)
    write_index(kb_root, entries)

    print("Indexed %d file%s." % (len(entries), "" if len(entries) == 1 else "s"))
    print("Wrote %s/INDEX.md and %s/_index.json" % (kb_root, kb_root))

    if problems:
        print("")
        print("%d file%s need attention:" % (len(problems), "" if len(problems) == 1 else "s"))
        for problem in problems:
            print("  - %s" % problem)
        print("")
        print("Run `python3 tools/check.py` for the details.")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001
        fail(exc)
