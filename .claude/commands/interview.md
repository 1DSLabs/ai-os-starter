---
description: Interview the owner one question at a time and turn new answers into labeled knowledge-base files.
disable-model-invocation: true
---

# Interview the owner

Help the user write down knowledge that currently lives in their head.

## Prepare

Read `CLAUDE.md`, `Knowledge_Base/INDEX.md`, and the knowledge files that appear relevant. Note what is already answered. Don't ask for information that those files already cover unless two sources conflict.

Ask what part of the business would be most useful to document first. If the user has no preference, start with the first uncovered topic below.

## Topics

Work through these topics in a natural order. Ask one question, wait for the answer, then choose the next question.

### Basics

Learn what the business offers, who it serves, the outcome customers or clients want, and which team roles own the main areas of work.

### Voice

Learn how the business should sound with customers or clients, how it should sound with the team, which words feel natural, which words should be avoided, and whether the tone changes by channel. Ask for a real example when a description such as "friendly" could mean several things.

### Processes

Pick one recurring process at a time. Learn its trigger, owner, inputs, steps, handoffs, exceptions, output, and what counts as done. Ask for the real sequence. Don't fill a missing step yourself.

### Rules

Learn how recurring decisions are made, what needs approval, which boundaries can't move, and when a team member should ask for help.

### Terms

Learn the words, abbreviations, product names, service names, and internal phrases that need an agreed meaning.

## Turn answers into files

When there is enough reliable detail for one or more useful files, summarize the proposed titles, types, folders, and one-line summaries. Ask one confirmation question before writing.

Write one idea per file in the matching folder under `Knowledge_Base/`. Every file must begin with a label block containing `id`, `title`, `type`, `summary`, and `updated`. Set `updated` to today's date in `YYYY-MM-DD` form. The valid types are `principle`, `framework`, `model`, `playbook`, `template`, `decision`, `glossary`, and `record`. Keep IDs unique, lowercase, and joined with dashes. Use short lowercase filenames joined with dashes. Add `owner`, `tags`, `aliases`, `status`, or `source` only when the answers support them.

Keep the user's words where they carry voice or judgment. Don't invent facts or turn a rough preference into a firm rule. Replace personal names, contact details, and account details with clear placeholders, then tell the user which kinds of details were replaced.

## Refresh and check

Check for Python 3 (`python3`, or `python`/`py` on Windows). From the repository root, try the matching form of these commands:

```bash
python3 tools/index.py
python3 tools/check.py
```

If both commands run, fix problems caused by the new or updated files, then rerun both. Report pre-existing problems without changing unrelated files unless the user asks. Say `All good` only when the check reports it.

If Python is missing or either command fails for any reason, don't leave the user at a raw error. Rebuild `Knowledge_Base/INDEX.md` by hand from every knowledge file's title and summary, tell the user the automated check was skipped, and carry on.

End by naming the files created or updated. Offer to continue with the next uncovered topic, one question at a time.
