# Skill format

A skill teaches Claude how to do a repeatable kind of work. Skills live in their own folders under `.claude/skills/` and are discovered automatically by Claude Code.

## Start from the included template

The included starting point is `.claude/skills/skill-template/SKILL.md`. Since folders beginning with a dot may be hidden on your computer, paste this prompt into Claude Code:

```text
Help me create a local skill using .claude/skills/skill-template/SKILL.md as the starting point. Ask what the skill should do and when it should run, then create it with a short lowercase folder name and a matching frontmatter name.
```

Keep words in the new name joined by hyphens.

Each skill starts with frontmatter:

```yaml
---
name: skill-template
description: Provide a valid starting point for a new local Claude skill. Use when the user wants to create, copy, structure, or improve a skill inside this business folder.
---
```

The `name` must match the new folder name. The `description` should say what the skill does and when Claude should use it.

## What goes in the instructions

Give Claude a clear outcome, the files it should read, the steps it should follow, and what a finished result must contain. Point to real files and folders in this project. Tell Claude to ask when required information is missing.

Keep business facts in `Knowledge_Base/`, not inside the skill. The skill explains the method. The knowledge files hold the voice, rules, examples, and process details that can change over time.

Test a new skill on a real task. If Claude has to guess, add the missing fact to the right knowledge file or tighten the instruction that led it astray.
