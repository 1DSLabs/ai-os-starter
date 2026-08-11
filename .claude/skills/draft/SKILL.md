---
name: draft
description: Draft customer, client, team, sales, marketing, or operational writing in the business's established voice using relevant knowledge-base files. Use when the user asks Claude to write, rewrite, edit, adapt, or respond on behalf of the business.
---

# Draft in the business voice

Write work that sounds consistent with the business and stays grounded in its recorded knowledge.

## Load the right context

1. Read `CLAUDE.md` for audience, tone, always and never guidance, and hard rules.
2. Read `Knowledge_Base/INDEX.md`.
3. Choose files by title and summary, based on the task. Principles, templates, decisions, glossary entries, frameworks, and relevant records may all matter.
4. Read the chosen files in full before drafting.

Use `python3 tools/find.py "<query>" --json` only when the index is missing, stale, or too large to scan. Treat every result as a candidate and inspect it before use. Don't accept the top keyword match without checking its meaning.

Files marked `status: example` show the format only. Never treat them as real policy, coverage, or an update target. If an example is the only match for a real question, say no real file covers it yet and offer to create one.

When the index can't be used, check for Python 3 (`python3`, or `python`/`py` on Windows). Python may be missing or the search command may fail. In either case, don't stop at the error. Scan the label blocks in the relevant `Knowledge_Base/` folders by hand, then choose files by title, summary, aliases, and meaning.

## Draft

Identify the audience, channel, purpose, desired action, and any length or format limit from the request. Ask one concise question when a missing fact would materially change the draft. Make a reasonable, low-risk choice for minor presentation details.

Match the voice shown in `CLAUDE.md` and relevant examples. Use approved terms from the glossary, apply recorded rules, and follow the closest useful template without forcing content into it.

Don't invent offers, proof, prices, deadlines, policies, or results. If knowledge files disagree, name the conflict and ask which source controls. Keep personal and sensitive data out of the draft unless the user has supplied it for this specific private use and the hard rules allow it.

Return the draft in the requested format. Keep notes and assumptions outside the draft so the user can copy the writing cleanly. Save or update a file only when the user asks.

End with a brief note naming the knowledge files used. If none were relevant, say that the draft relied on `CLAUDE.md` and the user's request.
