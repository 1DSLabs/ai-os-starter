# Knowledge file format

Each file in `Knowledge_Base/` holds one useful idea. A short label block at the very top tells Claude what the file covers and where it belongs.

## The label block

Start every knowledge file with this shape:

```yaml
---
id: project-handoff
title: Project Handoff
type: playbook
summary: The steps for handing completed work to a client.
updated: 2026-08-11
owner: Operations
tags: [delivery, handoff]
aliases: [closing a project]
status: active
source: Team walkthrough
---
```

Five fields are required:

| Field | What to write |
|---|---|
| `id` | A unique lowercase name with words joined by hyphens |
| `title` | A clear human-readable title |
| `type` | One of the eight types listed below |
| `summary` | One sentence that helps Claude decide when to read the file |
| `updated` | The last edit date in `YYYY-MM-DD` form |

The optional fields are `owner`, `tags`, `aliases`, `status`, and `source`. Use square brackets for short lists, as shown above. You can also put one list item on each following line:

```yaml
tags:
  - delivery
  - handoff
```

Colons are fine inside a value. Quotes are optional unless they make the value easier to read.

## Types and folders

The value of `type` must match the folder:

| Type | Folder | Use it for |
|---|---|---|
| `principle` | `Knowledge_Base/principles/` | Beliefs and standards that guide choices |
| `framework` | `Knowledge_Base/frameworks/` | Reusable ways to think through a problem |
| `model` | `Knowledge_Base/models/` | Named concepts and mental models |
| `playbook` | `Knowledge_Base/playbooks/` | Repeatable steps for a process |
| `template` | `Knowledge_Base/templates/` | Reusable starting copy or structure |
| `decision` | `Knowledge_Base/decisions/` | Rules for making a recurring choice |
| `glossary` | `Knowledge_Base/glossary/` | Terms with business-specific meanings |
| `record` | `Knowledge_Base/records/` | Dated context worth keeping |

## The body

Write normal Markdown below the closing three dashes. Keep one main idea per file. Add headings where they help, keep the owner's wording, and record uncertainty instead of filling gaps with invented details.

When you add or edit files, run:

```bash
python3 tools/index.py
python3 tools/check.py
```

The first command refreshes the index. The second reports missing labels, duplicate IDs, and files in the wrong folder.

