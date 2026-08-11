# How the folder works

Claude starts with `CLAUDE.md`, which gives it the business identity, voice, and hard rules. It reads the index to locate the few knowledge files that matter for a task. Commands help you add or retrieve material, while skills describe repeatable ways of working.

The Markdown files are the system. The Python tools are optional helpers for organizing and checking them.

## Index

Run `python3 tools/index.py` after adding or changing knowledge files. It reads their label blocks and writes two generated files:

- `Knowledge_Base/INDEX.md` is a table a person or Claude can scan.
- `Knowledge_Base/_index.json` maps each ID to its file path.

The `/ingest` and `/interview` commands refresh the index after they write files when Python 3 is available.

## Check

Run `python3 tools/check.py` to inspect every knowledge file. It catches missing required fields, duplicate IDs, unknown types, and files whose type doesn't match their folder. A clean run ends with `All good`.

Run it whenever you edit a label block by hand or move a file.

## Find

Run `python3 tools/find.py "refund" --top 3` to search titles, IDs, aliases, tags, summaries, and file bodies. Add `--json` when another tool needs structured output.

Claude's `/load` command reads `Knowledge_Base/INDEX.md` first and chooses files by title and summary. Keyword search is the fallback when the index is missing, stale, or too large to scan. A keyword score can miss a synonym, so Claude still judges whether a result fits before loading it.

## No Python required

You can create, read, and edit every file without running a script. If Python 3 isn't available, keep `Knowledge_Base/INDEX.md` current by hand. Follow the same sections and table columns already in the generated file.

