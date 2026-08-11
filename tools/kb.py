"""Shared helpers for the three tools.

Standard library only. Nothing to install.
"""

import os
import sys

KB_DEFAULT = "Knowledge_Base"

# The order sections appear in INDEX.md.
TYPE_ORDER = [
    "principle",
    "framework",
    "model",
    "playbook",
    "template",
    "decision",
    "glossary",
    "record",
]

# Folder name -> the type of file that belongs in it.
FOLDER_TYPES = {
    "principles": "principle",
    "frameworks": "framework",
    "models": "model",
    "playbooks": "playbook",
    "templates": "template",
    "decisions": "decision",
    "glossary": "glossary",
    "records": "record",
}

SKIP_FILES = {"INDEX.md"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}


def _repo_root():
    """The folder that holds tools/, found from this file's own location.

    This is what lets the tools work no matter which directory you run them
    from. A beginner will not know to `cd` first, and they should not have to.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_kb_root(candidate=KB_DEFAULT):
    """Find the Knowledge_Base folder, trying the obvious places in order."""
    tries = []

    if candidate:
        tries.append(os.path.abspath(candidate))
    tries.append(os.path.join(os.getcwd(), KB_DEFAULT))
    tries.append(os.path.join(_repo_root(), KB_DEFAULT))

    for path in tries:
        if os.path.isdir(path):
            return path

    raise SystemExit(
        "I couldn't find your Knowledge_Base folder.\n"
        "\n"
        "Looked in:\n"
        + "\n".join("  " + t for t in tries)
        + "\n\n"
        "Run this from inside your brain folder, like:\n"
        "  cd \"path/to/your brain folder\"\n"
        "  python3 tools/index.py\n"
    )


def iter_knowledge_files(kb_root, unreadable_paths=None):
    """Yield knowledge files and optionally collect folders os.walk cannot read."""
    def collect_walk_error(error):
        if unreadable_paths is not None:
            unreadable_paths.append(error.filename or kb_root)

    skip_files = {name.casefold() for name in SKIP_FILES}
    for current, dirnames, filenames in os.walk(kb_root, onerror=collect_walk_error):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            folded_name = name.casefold()
            if not folded_name.endswith(".md") or folded_name in skip_files:
                continue
            if folded_name.startswith("_readme") or name.startswith("."):
                continue
            yield os.path.join(current, name)


def folder_of(kb_root, path):
    """The top-level Knowledge_Base folder a file sits in, or None."""
    rel = os.path.relpath(path, kb_root)
    parts = rel.split(os.sep)
    return parts[0] if len(parts) > 1 else None


def fail(exc):
    """Report an unexpected error in plain English instead of a traceback."""
    sys.stderr.write(
        "Something went wrong and the tool stopped.\n"
        "\n"
        "  %s: %s\n"
        "\n"
        "This is usually a file that got saved in an odd format. Try\n"
        "`python3 tools/check.py` to see which file it is.\n" % (type(exc).__name__, exc)
    )
    sys.exit(1)
