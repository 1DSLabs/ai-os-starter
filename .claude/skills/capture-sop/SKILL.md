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

Learn the process name, purpose, trigger, owner role, inputs, steps, handoffs, exceptions, output, and definition of done. Ask one focused question at a time for any missing detail that changes how someone would perform the work. Don't invent steps or turn an assumption into a rule.

Keep personal names, contact details, account details, and other sensitive values out of the playbook. Replace them with role-based or descriptive placeholders and tell the user what kind of information was replaced.

## Write the playbook

Create one Markdown file in `Knowledge_Base/playbooks/`. Use a short lowercase filename joined with dashes. Begin with this label structure:

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

Check for Python with `command -v python3`.

If Python is available, run these commands from the repository root:

```bash
python3 "tools/index.py"
python3 "tools/check.py"
```

Fix any problem caused by the playbook and rerun the checks until they pass.

If Python isn't available, update `Knowledge_Base/INDEX.md` by hand from the knowledge files and explain that the automated check was skipped.

Report the file created or updated, the gaps that remain, and any sensitive details replaced with placeholders.
