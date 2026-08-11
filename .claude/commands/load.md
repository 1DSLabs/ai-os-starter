---
description: Load the smallest useful set of knowledge files for a task, choosing from the index before using keyword search.
---

# Load relevant knowledge

The user's request is:

$ARGUMENTS

If the request is empty or unclear, ask what they want to work on before loading files.

## Retrieval order

1. Read `CLAUDE.md` for identity, voice, and hard rules.
2. Read `Knowledge_Base/INDEX.md` first.
3. Compare the request with the titles and summaries in the index. Use judgment to choose the smallest set of files that can answer the request well.
4. Read each chosen file in full. Follow useful links only when the task needs them.

Use keyword search only when `Knowledge_Base/INDEX.md` is missing, stale, or too large to scan. Stale means the index no longer matches the files actually in the folders.

Check for Python 3 (`python3`, or `python`/`py` on Windows). Then try the matching form of `python3 tools/find.py "<query>" --json`. Replace `<query>` with a short phrase made only of letters, numbers, and spaces. Keep it as one quoted argument.

Search results are candidates, not answers. Inspect their titles, summaries, and contents before deciding what to load. Never load the top keyword result blindly because a synonym can point to the wrong file.

Files marked `status: example` show the format only. Never treat them as real policy, coverage, or an update target. If an example is the only match for a real question, say no real file covers it yet and offer to create one.

When the index can't be used, Python may be missing or the search command may fail. In either case, don't stop at the error. Scan the label blocks in the relevant `Knowledge_Base/` folders by hand, then choose files by title, summary, aliases, and meaning.

Don't load the full knowledge base as a default. When sources conflict or a required fact is missing, tell the user and ask instead of guessing.

After loading, name the files you used in one short line, then do the requested task. If the user only asked to load context, summarize what is ready and wait for their next instruction.
