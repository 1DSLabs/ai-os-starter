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

## Before you start

You need a [Claude account](https://claude.ai) on a paid plan. Claude Code comes with Claude Pro and Max plans (and most Team plans).

Choose where you want to work: use the Claude desktop app on your computer, or use Claude Code on the web in your browser. Desktop keeps the folder on your machine; web needs no install and uses a private GitHub copy.

If Claude Code on Windows asks for Git, install Git for Windows from [git-scm.com](https://git-scm.com).

## Install

### Path A: on your computer (Claude desktop app)

1. Download the [Claude desktop app](https://claude.ai/download) and sign in.
2. Open the [AI OS Starter repository](https://github.com/1DSLabs/ai-os-starter), choose **Code**, then choose **Download ZIP**. Unzip it. The unzipped folder is named `ai-os-starter-main`; rename it to anything you like, such as `My Business Brain`.
3. In the desktop app, open Claude Code and choose **Open folder**. Select the folder that contains `START-HERE.md`.
4. Type `/setup`.

### Path B: in your browser (Claude Code on the web)

1. Create a free [GitHub account](https://github.com) if you don't have one.
2. On the [AI OS Starter repository](https://github.com/1DSLabs/ai-os-starter), choose **Use this template**, then **Create a new repository**. Name it, for example `my-business-brain`, and set it to **Private**. The private setting matters because your business is going in here.
3. Go to [Claude Code on the web](https://claude.ai/code), sign in, connect your GitHub account, and open the repository you just created.
4. Type `/setup`.
5. When you finish a browser session, tell Claude to commit and push your work so it's saved to the repository.

Don't fork the public repository for real business use because a fork of a public repository stays public; **Use this template** is the private path.

**Self-check:** Type `/` and look at the list. If you see `setup`, `ingest`, `interview`, and `load`, you're in the right place. If you don't, you opened the wrong folder; open the one containing `START-HERE.md`.

Already use Git? Run `git clone https://github.com/1DSLabs/ai-os-starter.git "My Business Brain"`, then open the new folder in the Claude desktop app.

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
| `Knowledge_Base/models/` | Named concepts, calculations, or mental models |
| `Knowledge_Base/playbooks/` | Repeatable process steps |
| `Knowledge_Base/templates/` | Reusable starting copy or structure |
| `Knowledge_Base/decisions/` | Rules for recurring choices |
| `Knowledge_Base/glossary/` | Terms with a specific meaning in your business |
| `Knowledge_Base/records/` | Dated context worth keeping |

## The optional tools

- Rebuild the readable index and JSON map with `python3 tools/index.py`.
- Find missing labels, duplicate IDs, and misplaced files with `python3 tools/check.py`.
- Search the knowledge files with `python3 tools/find.py "refund" --top 3`.

The scripts need no extra packages. They use Python 3, which is already on your Mac. On Windows, install Python from [python.org](https://www.python.org/downloads/) or skip the tools entirely. Everything works without them.

On Windows, use `python` (or `py`) instead of `python3` in these commands.

## Keep it private

The content Claude reads is sent to Anthropic to generate responses, under your own Claude account's terms and settings. The folder itself is plain files on your computer or, on the web path, in your private GitHub repository, and 1DS Collective never sees any of it. Treat it like your books: keep the repository private, review it before sharing, and don't store real customer or employee names, contact information, account numbers, health details, or financial details.

## FAQ

### Do I need to code?

No. You can use the commands in Claude Code and edit the Markdown files like normal text. The optional tools are short Python scripts, but the folder works without them.

### What if I have no SOPs or written processes?

Type `/interview`. Claude asks one question at a time and turns your answers into the first small knowledge files. Rough answers are useful. You can improve them as the business changes.

### Does my data get uploaded anywhere?

The content Claude reads is sent to Anthropic to generate responses, under your own Claude account's terms and settings. The folder itself is plain files on your computer or, on the web path, in your private GitHub repository. 1DS Collective never sees any of it.

### Can my team use it too?

Yes. Put a reviewed copy in a private place your team can access, agree on who owns each area, and keep the labels current. Remove personal data before sharing.

### What's the difference between a command and a skill?

Commands and skills are both packaged instructions. A command is something you type deliberately, such as `/ingest`. A skill is a method Claude can also pick up on its own when a task fits.

### How do I update to a newer version?

Before updating, back up your filled `CLAUDE.md`, your own material in `Knowledge_Base/` and `_inbox/`, and any skills or commands you created under `.claude/`. Download the new release into a separate folder, read its release notes, then copy your material over after reviewing any format changes. Don't overwrite your working folder without a backup.

## Who built this

[1DS Collective](https://1dscollective.com) built AI OS Starter from the system we run our own agency on. We made this public so a business of any size can start with a useful structure.
