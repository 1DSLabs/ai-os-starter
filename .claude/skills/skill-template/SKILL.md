---
name: skill-template
description: Provide a valid starting point for a new local Claude skill. Use when the user wants to create, copy, structure, or improve a skill inside this business folder.
---

# Create a local skill

Build a focused skill that teaches Claude one repeatable way of working.

## Make the skill

1. Clarify the skill's job, trigger requests, expected output, needed inputs, and firm guardrails. Ask the user about any missing choice that would change the workflow.
2. Copy this folder inside `.claude/skills/`.
3. Give the copy a short name made from lowercase letters, numbers, and single dashes. Match the folder name to the `name` value.
4. Replace the frontmatter description with one sentence that says what the skill does and when it should run.
5. Replace this body with direct instructions for completing the task.
6. Keep only the context, steps, guardrails, and finishing checks the task needs.

Use this complete starting point for the copy's skill instruction file:

```markdown
---
name: your-skill-name
description: Explain what this skill does and the requests that should trigger it.
---

# Skill title

State the outcome in one sentence.

## Prepare

Read the files needed for this work. Include `CLAUDE.md` and `Knowledge_Base/INDEX.md` when business identity or recorded knowledge matters.

## Do the work

1. Put the first required action here.
2. Put the next required action here.
3. Add a decision rule where the right action depends on context.

## Guardrails

- State what must stay true.
- State what Claude must never guess or change.
- Say when to ask the user a question.

## Finish

Check the result, fix failures, and report what changed.
```

Keep the frontmatter to `name` and `description`. Put trigger wording in the description because Claude reads it before the body. Write body instructions as actions. Refer only to files that exist, and test every command the skill tells Claude to run.

Before finishing, confirm that the copy contains its skill instruction file, its folder and `name` match, its description explains both purpose and trigger, and every referenced path resolves from the repository root.
