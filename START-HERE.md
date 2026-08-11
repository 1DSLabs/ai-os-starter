# Start here

Whether you opened this folder on your computer or connected it through [claude.ai/code](https://claude.ai/code), the experience inside is the same. Your first session has two jobs: tell Claude the basics about the business, then give it a little real material to organize.

## 1. Set up the identity file

Type this in Claude Code:

```text
/setup
```

The conversation will feel like this:

> **Claude:** What's the business called?
>
> **You:** Northstar Studio.
>
> **Claude:** What do you do, and who do you help?
>
> **You:** We help small service companies explain and package what they sell.
>
> **Claude:** How should customer-facing writing sound?
>
> **You:** Clear, warm, and direct. No hype.

Claude continues one question at a time through team tone, always and never lists, and hard rules. It then fills `CLAUDE.md` with your answers. Read the result and change anything that doesn't sound right.

Want to preview a completed identity file? See `docs/example-CLAUDE.md` for the fictional Northstar Studio version.

## 2. Add what you already know

If you have useful documents, choose two or three to start. Good choices include a process guide, an FAQ, meeting notes, a policy, or a strong email example.

Remove personal data, then place copies in `_inbox/`. Type:

```text
/ingest
```

Claude reads the source material and proposes a short file list, including a destination folder and one-line summary for each file. It stops there. Review the list, ask for changes if needed, and approve it when it looks right.

After approval, Claude writes the files, tries to refresh the index and check the labels, then tells you what changed. If the scripts can't run, it rebuilds the readable index by hand and carries on. It keeps the owner's wording and calls out source details it replaced with placeholders.

If you have nothing written down yet, type `/interview` instead. Claude asks about the business basics, voice, processes, rules, and terms. It skips what your files already cover and asks one question at a time.

## 3. See what a finished file looks like

Four fictional examples ship with the folder:

- Writing principle: `Knowledge_Base/principles/EXAMPLE-how-we-write.md`
- Onboarding process: `Knowledge_Base/playbooks/EXAMPLE-new-client-onboarding.md`
- Kickoff email: `Knowledge_Base/templates/EXAMPLE-project-kickoff-email.md`
- Refund rule: `Knowledge_Base/decisions/EXAMPLE-refund-requests.md`

Each starts with the same label block your files will use. The summary helps Claude decide whether to read it, while the body holds the useful detail. Delete the examples once your real files cover those jobs.

Browse `Knowledge_Base/INDEX.md` to see every file grouped by type. Every category has a guide like `Knowledge_Base/principles/_README.md` that explains what belongs there.

## 4. Ask for real work

Try a task you already need done:

> Draft a kickoff email for the project we discussed. Use our normal voice and process.

Claude should find and read the relevant knowledge before drafting. If a fact is missing, it should ask instead of guessing. Your answer can become another knowledge file when it will help next time.

## 5. Write your first skill

Skills give Claude a repeatable method for a kind of work. The included `draft` skill writes in your voice, and `capture-sop` turns a process description into a playbook.

When you notice another task repeating, paste this into Claude Code:

```text
Help me create a local skill using .claude/skills/skill-template/SKILL.md as the starting point. Ask what the skill should do and when it should run, then create it with a matching folder name and frontmatter name.
```

Claude can work with the hidden folder for you. Follow `docs/skill-format.md` for the full format.

Keep changing business facts in the knowledge base. Put only the repeatable method in the skill.

## 6. Use the tools when they help

You can ignore the Python tools at first. The Markdown structure and Claude commands are enough to begin.

Once you edit knowledge files by hand, these commands help keep them tidy:

```bash
python3 tools/index.py
python3 tools/check.py
python3 tools/find.py "project kickoff" --top 3
```

Run them from this folder's top level. They need Python 3 and no extra packages. See `docs/how-it-works.md` for what each one does.

## As you grow

Keep shared principles, terms, and company-wide rules in one common folder. When a location or brand develops distinct processes, give it a clearly named area and keep only its specific material there. Duplicate as little as possible, and state which rule wins when shared and local guidance differ.

Treat this folder like your books. Keep it private, review it before sharing, and never store real customer or employee names, contact information, account numbers, health details, or financial details in it.
