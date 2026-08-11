---
name: capture-sop
description: Turn a process the user describes into a reusable, labeled playbook in the business knowledge base. Use when the user explains how work gets done, asks to document a process, or wants an SOP, checklist, or repeatable workflow captured.
---

# Capture a process

Create a faithful playbook from the user's real process.

## Gather context

1. Read `CLAUDE.md`.
2. Open `Knowledge_Base/INDEX.md`.
3. Review existing playbooks, principles, decisions, templates, and glossary entries that may affect this process.
4. Decide whether the user is adding a new process or updating an existing one. Don't overwrite a related file unless the user has asked to update it.

If the index is missing or stale, scan the label blocks in the relevant `Knowledge_Base/` folders by hand before deciding what already exists.

Files marked `status: example` show the format only. Never treat them as real policy, coverage, or an update target. If an example is the only match for a real question, say no real file covers it yet and offer to create one.

Learn the process name, purpose, trigger, owner role, inputs, steps, handoffs, exceptions, output, and definition of done. Ask one focused question at a time for any missing detail that changes how someone would perform the work. Don't invent steps or turn an assumption into a rule.

Keep personal names, contact details, account details, and other sensitive values out of the playbook. Replace them with role-based or descriptive placeholders and tell the user what kind of information was replaced.

## Show the draft and get approval

Before creating or updating any file, show the user the full draft or a faithful summary that includes every proposed section, step, exception, and open gap. Ask for a clear yes. Don't create, edit, move, or delete any file before that yes.

## Write the playbook

After approval, create one Markdown file in `Knowledge_Base/playbooks/`. Use a short lowercase filename joined with dashes. Begin with this label structure:

```yaml
---
id: unique-lowercase-id
title: Clear process title
type: playbook
summary: One sentence describing when this process is useful.
updated: YYYY-MM-DD
---
```

Add optional `owner`, `tags`, `aliases`, `status`, or `source` fields only when the conversation or an existing source supports them.

Set `updated` to today's date in `YYYY-MM-DD` form. Confirm that the ID is unique before writing.

Use only the sections the process needs. A useful order is:

1. Purpose
2. When to use it
3. Owner
4. Inputs
5. Steps
6. Exceptions and handoffs
7. Done when

Write steps as clear actions in the order they happen. Keep the user's terminology. Link to an existing knowledge file when it contains a rule or template needed for a step. Don't copy the same guidance into two files.

## Finish cleanly

Check for Python 3 (`python3`, or `python`/`py` on Windows). From the repository root, try the matching form of these commands:

```bash
python3 tools/index.py
python3 tools/check.py
```

If both commands run, fix problems caused by the new or updated playbook, then rerun both. Report pre-existing problems without changing unrelated files unless the user asks. Say the full check passed only when it did.

If Python is missing or either command fails for any reason, don't leave the user at a raw error. Update `Knowledge_Base/INDEX.md` by hand from the knowledge files, explain that the automated check was skipped, and carry on.

Report the file created or updated, the gaps that remain, and any sensitive details replaced with placeholders.
