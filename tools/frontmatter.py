"""Read the label block at the top of a knowledge file.

No installs, no dependencies. Python 3.8+ standard library only.

A label block is the small chunk between the first pair of `---` lines:

    ---
    id: new-customer-intake
    title: New Customer Intake
    type: playbook
    summary: The steps for welcoming a new customer.
    updated: 2026-08-11
    tags: [intake, sales]
    ---

Values come back as strings, except lists, which come back as lists of
strings. Nothing is coerced: `updated: 2026-06-20` stays the text
"2026-06-20", and `owner: Yes` stays "Yes" rather than becoming a boolean.
That is deliberate. Silent type coercion is the most common way these files
break.
"""

import re

# The opening --- must be the very first thing in the file. Tolerates a UTF-8
# BOM (Word and some editors add one) and Windows CRLF line endings.
_DELIMITER = re.compile(r"---[ \t]*$")

_INLINE_LIST = re.compile(r"^\[(.*)\]$")

# Curly quotes, which arrive whenever someone pastes out of Word or Google Docs.
_SMART_QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})


class LabelBlockError(Exception):
    """Raised when a label block exists but cannot be understood."""


def _strip_quotes(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _split_list(body):
    items = []
    depth = 0
    current = ""
    for char in body:
        if char in "[(":
            depth += 1
        elif char in "])":
            depth -= 1
        if char == "," and depth == 0:
            items.append(current)
            current = ""
        else:
            current += char
    items.append(current)
    return [_strip_quotes(i) for i in items if i.strip()]


def parse(text):
    """Return the label block as a dict, or None if the file has no block.

    Raises LabelBlockError when a block is present but malformed.
    """
    lines = text.splitlines()
    if not lines:
        return None

    first_line = lines[0]
    if first_line.startswith("﻿"):
        first_line = first_line[1:]
    if not _DELIMITER.fullmatch(first_line):
        return None

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if _DELIMITER.fullmatch(line):
            closing_index = index
            break
    if closing_index is None:
        raise LabelBlockError(
            "the label block starts on line 1 but has no closing `---` line"
        )

    fields = {}
    key_lines = {}
    pending_key = None

    for lineno, raw in enumerate(lines[1:closing_index], start=2):
        line = raw.translate(_SMART_QUOTES).replace("\t", "    ").rstrip()

        if not line.strip() or line.lstrip().startswith("#"):
            continue

        # A "- item" line continues the list started by the previous key.
        bullet = re.match(r"^\s*-\s+(.*)$", line)
        if bullet:
            if pending_key is None:
                raise LabelBlockError(
                    "line %d: found a list item (%s) before any label name"
                    % (lineno, line.strip())
                )
            if fields[pending_key] == "":
                fields[pending_key] = []
            elif not isinstance(fields[pending_key], list):
                raise LabelBlockError(
                    "line %d: `%s` already has a single value on line %d, "
                    "so it can't also have a list"
                    % (lineno, pending_key, key_lines[pending_key])
                )
            fields[pending_key].append(_strip_quotes(bullet.group(1)))
            continue

        if ":" not in line:
            raise LabelBlockError(
                'line %d: "%s" is missing a colon. Every label line looks like '
                "`name: value`." % (lineno, line.strip())
            )

        key, _, value = line.partition(":")
        key = key.strip()
        if not key:
            raise LabelBlockError('line %d: missing a label name before the colon' % lineno)
        if key in fields:
            raise LabelBlockError(
                "duplicate key `%s` on line %d (first set on line %d)"
                % (key, lineno, key_lines[key])
            )

        value = value.strip()
        pending_key = key
        key_lines[key] = lineno

        if not value:
            # Either a key whose list follows on the next lines, or an empty value.
            fields[key] = ""
            continue

        inline = _INLINE_LIST.match(value)
        if inline:
            fields[key] = _split_list(inline.group(1))
            continue

        fields[key] = _strip_quotes(value)

    return fields


def read(path):
    """Parse the label block of a file at `path`. Returns dict or None."""
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return parse(handle.read())
