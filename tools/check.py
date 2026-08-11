#!/usr/bin/env python3
"""Check your knowledge files for problems.

Confirms every file has a proper label block, that no two files share an id,
and that files sit in the folder that matches their type.

    python3 tools/check.py

Prints "All good" and exits 0 when everything is fine.
No installs required. Python 3 standard library only.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontmatter import LabelBlockError, read  # noqa: E402
from kb import (  # noqa: E402
    FOLDER_TYPES,
    KB_DEFAULT,
    fail,
    folder_of,
    iter_knowledge_files,
    resolve_kb_root,
)

REQUIRED = ("id", "title", "type", "summary", "updated")
TYPES = set(FOLDER_TYPES.values())
LONG_FILE_LINES = 400


def check_file(kb_root, path):
    """Return (problems, suggestions, id_or_None) for one file."""
    rel = os.path.relpath(path, kb_root).replace(os.sep, "/")
    problems = []
    suggestions = []

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    except OSError as exc:
        return ["%s: could not open it (%s)" % (rel, exc)], [], None

    try:
        labels = read(path)
    except LabelBlockError as exc:
        return ["%s: %s" % (rel, exc)], [], None

    if labels is None:
        return [
            "%s: no label block. Add one at the very top of the file, "
            "starting and ending with a line of three dashes." % rel
        ], [], None

    for field in REQUIRED:
        if not labels.get(field):
            problems.append("%s: missing `%s` in the label block" % (rel, field))

    file_type = labels.get("type")
    if file_type and file_type not in TYPES:
        problems.append(
            "%s: `type: %s` isn't one I know. Use one of: %s"
            % (rel, file_type, ", ".join(sorted(TYPES)))
        )

    folder = folder_of(kb_root, path)
    expected = FOLDER_TYPES.get(folder)
    if expected and file_type and file_type != expected:
        problems.append(
            "%s: it's in `%s/` (which holds `%s` files) but its type is `%s`. "
            "Move the file or change the type." % (rel, folder, expected, file_type)
        )

    entry_id = labels.get("id")
    if entry_id:
        if entry_id != entry_id.lower() or " " in entry_id:
            problems.append(
                "%s: id `%s` should be lowercase with dashes instead of spaces"
                % (rel, entry_id)
            )

    summary = labels.get("summary", "")
    if summary and len(summary) > 200:
        suggestions.append("%s: the summary is long. One sentence works best." % rel)

    line_count = text.count("\n") + 1
    if line_count > LONG_FILE_LINES:
        suggestions.append(
            "%s: %d lines. Long files can be harder to scan. Consider splitting it in two."
            % (rel, line_count)
        )

    return problems, suggestions, entry_id


def main(argv):
    kb_root = resolve_kb_root(argv[1] if len(argv) > 1 else KB_DEFAULT)

    problems = []
    suggestions = []
    ids = {}
    count = 0

    for path in iter_knowledge_files(kb_root):
        count += 1
        file_problems, file_suggestions, entry_id = check_file(kb_root, path)
        problems.extend(file_problems)
        suggestions.extend(file_suggestions)
        if entry_id:
            rel = os.path.relpath(path, kb_root).replace(os.sep, "/")
            ids.setdefault(entry_id, []).append(rel)

    for entry_id, paths in sorted(ids.items()):
        if len(paths) > 1:
            problems.append(
                "the id `%s` is used by %d files: %s. Ids must be unique."
                % (entry_id, len(paths), ", ".join(paths))
            )

    if count == 0:
        print("No knowledge files yet. Nothing to check.")
        print("Add some with `/ingest` or `/interview` in Claude Code.")
        return 0

    for suggestion in suggestions:
        print("suggestion: %s" % suggestion)

    if problems:
        if suggestions:
            print("")
        for problem in problems:
            print("problem: %s" % problem)
        print("")
        print(
            "%d problem%s across %d file%s."
            % (len(problems), "" if len(problems) == 1 else "s", count, "" if count == 1 else "s")
        )
        print("Fix those and run this again.")
        return 1

    print(
        "All good. %d file%s checked, no problems."
        % (count, "" if count == 1 else "s")
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001
        fail(exc)
