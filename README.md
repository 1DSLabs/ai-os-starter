# AI OS Starter

Write your business down once, then give Claude the context to do consistent work every time.

## What this is

AI OS Starter is a folder for the facts, processes, voice, rules, and examples that make your business yours. Claude reads those small files before it works, so each conversation starts with useful context instead of a blank page.

It works for any business. You don't need a new platform or anything beyond Claude Code, and the folder still works as plain Markdown if you skip every optional script.

## What you get

```text
AI-OS-Starter/
├── README.md              Public guide, install choices, privacy, and FAQ
├── START-HERE.md          Your first-session walkthrough
├── CLAUDE.md              Business identity, voice, and hard rules
├── .claude/
│   ├── commands/          Four guided commands for setup, capture, and retrieval
│   └── skills/            Repeatable instructions Claude discovers automatically
├── Knowledge_Base/        Small files grouped by the kind of knowledge they hold
├── _inbox/                Dropzone for material you want Claude to sort
├── tools/                 Optional Python helpers for index, checks, and search
└── docs/                  References for file, skill, and tool behavior
```

## Install

1. Download the ZIP without Git.

   Open the [AI OS Starter repository](https://github.com/1DSLabs/ai-os-starter), choose **Code**, then choose **Download ZIP**. Unzip it anywhere you can find again. In the Claude Code desktop app, choose **Open folder** and select the unzipped folder.

2. Or clone it with Git.

   Open a terminal, paste this command, and press Enter:

   ```bash
   git clone https://github.com/1DSLabs/ai-os-starter.git "My Business Brain"
   ```

   In the Claude Code desktop app, choose **Open folder** and select the new folder named My Business Brain.

3. Open an existing copy in the Claude Code desktop app.

   Choose **Open folder** and select its top-level folder, the one containing `START-HERE.md`.

For your 60-second first session, type `/setup`. Claude will ask one question at a time and fill in your business identity file with you.

## Your first 10 minutes

1. Type `/setup` and answer the short questions about your business, voice, and rules.
2. Choose the route that matches what you have:
   - If you have written material, put two or three useful documents in `_inbox/`, then type `/ingest`.
   - If little is written down, type `/interview` and build the first files through a conversation.
3. Give Claude a real task, such as drafting an email or walking through a process. Watch it read the relevant files before it answers.

Claude shows you its proposed files before `/ingest` writes them. You stay in control of what becomes part of the system.

## How it stays organized

Each knowledge file covers one main idea and starts with a small label block. The labels give it a unique ID, title, type, summary, and update date. Details live in [the file-format reference](docs/file-format.md).

| Folder | What belongs there |
|---|---|
| `Knowledge_Base/principles/` | Beliefs and standards that guide choices |
| `Knowledge_Base/frameworks/` | Reusable ways to think through a problem |
| `Knowledge_Base/models/` | Named concepts and mental models |
| `Knowledge_Base/playbooks/` | Repeatable process steps |
| `Knowledge_Base/templates/` | Reusable starting copy or structure |
| `Knowledge_Base/decisions/` | Rules for recurring choices |
| `Knowledge_Base/glossary/` | Terms with a specific meaning in your business |
| `Knowledge_Base/records/` | Dated context worth keeping |

## The optional tools

- Rebuild the readable index and JSON map with `python3 tools/index.py`.
- Find missing labels, duplicate IDs, and misplaced files with `python3 tools/check.py`.
- Search the knowledge files with `python3 tools/find.py "refund" --top 3`.

There are no installs. The tools use Python 3, which is already on your Mac. On Windows, install Python from [python.org](https://www.python.org/downloads/) or skip the tools entirely. Everything works without them.

## Keep it private

Your business goes in here, so treat the folder like your books. Keep the repository private if you push it anywhere, and review its contents before placing it on a shared drive.

Don't add real customer or employee personal data. Leave out names, contact information, account numbers, health details, and financial details. Replace sensitive source details with placeholders before saving them.

## FAQ

### Do I need to code?

No. You can use the commands in Claude Code and edit the Markdown files like normal text. The optional tools are short Python scripts, but the folder works without them.

### What if I have no SOPs or written processes?

Type `/interview`. Claude asks one question at a time and turns your answers into the first small knowledge files. Rough answers are useful. You can improve them as the business changes.

### Does my data get uploaded anywhere?

These files stay in the folder you choose unless you sync, share, or push that folder somewhere. When you use Claude Code, the content Claude reads is handled under the terms and settings of your Claude account. Check your current account settings and provider terms before adding confidential material.

### Can my team use it too?

Yes. Put a reviewed copy in a private place your team can access, agree on who owns each area, and keep the labels current. Remove personal data before sharing.

### What's the difference between a command and a skill?

A command is something you start, such as `/ingest` or `/load`. A skill is a reusable method Claude can pick up when a task fits, such as drafting in your voice or capturing a process.

### How do I update to a newer version?

Keep your filled `CLAUDE.md` and your own material in `Knowledge_Base/` and `_inbox/` safe. Download the new release into a separate folder, read its release notes, then copy your material over after reviewing any format changes. Don't overwrite your working folder without a backup.

## Who built this

[1DS Collective](https://1dscollective.com) built AI OS Starter from the system we run our own agency on. We made this public so a business of any size can start with a useful structure.
