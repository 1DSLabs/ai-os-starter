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
import tempfile
from datetime import datetime, timezone
from urllib.parse import quote

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


def build(kb_root, skipped_paths=None):
    """Return (entries_by_id, problems)."""
    entries = {}
    seen_ids = {}
    problems = []
    unreadable_paths = []

    for path in iter_knowledge_files(kb_root, unreadable_paths):
        rel = os.path.relpath(path, kb_root).replace(os.sep, "/")
        try:
            labels = read(path)
        except LabelBlockError as exc:
            problems.append("%s: %s" % (rel, exc))
            continue
        except OSError as exc:
            problems.append("%s: could not open it (%s)" % (rel, exc))
            continue

        if not labels or not labels.get("id"):
            if skipped_paths is not None:
                skipped_paths.append(rel)
            continue

        entry_id = labels["id"]
        if isinstance(entry_id, list):
            problems.append("%s: `id` must be a single value, not a list" % rel)
            continue
        if entry_id in seen_ids:
            problems.append(
                "two files share the id '%s': %s and %s"
                % (entry_id, seen_ids[entry_id], rel)
            )
            continue

        seen_ids[entry_id] = rel
        entries[entry_id] = {"path": rel, "labels": labels}

    for path in sorted(set(unreadable_paths)):
        rel = os.path.relpath(path, kb_root).replace(os.sep, "/")
        problems.append("%s: could not read this folder" % rel)

    return entries, problems


def _cell(value):
    """Make a value safe to drop into a markdown table cell."""
    text = " ".join(str(value).split())
    return text.replace("|", "\\|")


def render_index(entries, now=None):
    """Build the complete INDEX.md contents in memory."""
    by_type = {}
    for entry_id, entry in entries.items():
        file_type = entry["labels"].get("type") or "other"
        if not isinstance(file_type, str):
            file_type = "other"
        by_type.setdefault(file_type, []).append(entry_id)

    now = now or datetime.now(timezone.utc)
    generated = now.strftime("%Y-%m-%d %H:%M UTC")

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
            name = labels.get("title") or entry_id
            if labels.get("status") == "example":
                name = "%s (example)" % name
            lines.append(
                "| [%s](%s) | %s | %s | %s |"
                % (
                    _cell(name),
                    quote(path, safe="/"),
                    _cell(labels.get("summary", "")),
                    _cell(labels.get("owner", "")),
                    _cell(labels.get("updated", "")),
                )
            )
        lines.append("")

    return "\n".join(lines)


def render_map(entries, now=None):
    """Build the complete _index.json contents in memory."""
    now = now or datetime.now(timezone.utc)
    payload = {
        "version": VERSION,
        "generated": now.isoformat(),
        "files": {k: v["path"] for k, v in sorted(entries.items())},
    }
    return json.dumps(payload, indent=2) + "\n"


def _atomic_write(path, contents):
    """Replace path with complete contents written beside it."""
    directory = os.path.dirname(path)
    prefix = ".%s." % os.path.basename(path)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=directory, prefix=prefix, suffix=".tmp", delete=False
        ) as handle:
            temp_path = handle.name
            handle.write(contents)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None:
            try:
                os.unlink(temp_path)
            except FileNotFoundError:
                pass


def write_index(kb_root, entries):
    """Build and atomically write INDEX.md."""
    _atomic_write(os.path.join(kb_root, "INDEX.md"), render_index(entries))


def write_map(kb_root, entries):
    """Build and atomically write _index.json."""
    _atomic_write(os.path.join(kb_root, "_index.json"), render_map(entries))


def main(argv):
    kb_root = resolve_kb_root(argv[1] if len(argv) > 1 else KB_DEFAULT)
    skipped_paths = []
    entries, problems = build(kb_root, skipped_paths)

    now = datetime.now(timezone.utc)
    map_contents = render_map(entries, now)
    index_contents = render_index(entries, now)
    _atomic_write(os.path.join(kb_root, "_index.json"), map_contents)
    _atomic_write(os.path.join(kb_root, "INDEX.md"), index_contents)

    if skipped_paths:
        print(
            "Indexed %d files, skipped %d without labels: %s"
            % (len(entries), len(skipped_paths), ", ".join(skipped_paths))
        )
    else:
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
