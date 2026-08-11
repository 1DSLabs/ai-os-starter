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

Use keyword search only when `Knowledge_Base/INDEX.md` is missing, stale, or too large to scan. If Python is available, run `python3 "tools/find.py" "<query>" --json`, replacing `<query>` with a concise search phrase from the user's request and keeping it as one quoted argument.

Search results are candidates, not answers. Inspect their titles, summaries, and contents before deciding what to load. Never load the top keyword result blindly because a synonym can point to the wrong file.

If Python isn't available and the index can't be used, scan the label blocks in the relevant `Knowledge_Base/` folders by hand. Choose files by title, summary, aliases, and meaning.

Don't load the full knowledge base as a default. When sources conflict or a required fact is missing, tell the user and ask instead of guessing.

After loading, name the files you used in one short line, then do the requested task. If the user only asked to load context, summarize what is ready and wait for their next instruction.
