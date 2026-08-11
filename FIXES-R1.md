# FIX ROUND 1 (boss-approved findings; implement all)

Apply every fix below to the existing build in this directory. PLAN.md's non-negotiables
still bind, especially the voice rules and the beginner-proof rule. After the fixes,
re-run every acceptance check in PLAN.md plus the new checks at the bottom.

## F1 (P0): "Before you start" + dual-surface install in README.md

The install section currently assumes Claude Code is already on the reader's machine.
The audience includes people who have NEVER used Claude Code. Rebuild the install story:

Replace the current "Install" section with two sections:

### "Before you start"
- You need a Claude account on a paid plan. One plain sentence: Claude Code comes with
  Claude Pro and Max plans (and most Team plans). Link https://claude.ai
- Then a one-line chooser: work on your computer with the Claude desktop app, or work
  in your browser with Claude Code on the web. One sentence on how to pick: desktop
  keeps the folder on your machine; web needs no install and uses a private GitHub copy.

### "Install"
**Path A: on your computer (Claude desktop app)**
1. Download the Claude desktop app from https://claude.ai/download and sign in.
2. Download this folder: on the GitHub page, Code -> Download ZIP. Unzip it. The
   unzipped folder is named `ai-os-starter-main`; rename it to anything you like,
   such as `My Business Brain`.
3. In the desktop app, open Claude Code and choose Open folder. Select the folder
   that contains `START-HERE.md`.
4. Type `/setup`.

**Path B: in your browser (Claude Code on the web)**
1. Create a free GitHub account at https://github.com if you don't have one.
2. On this repository's page, choose **Use this template**, then **Create a new
   repository**. Name it (for example `my-business-brain`) and set it to **Private**.
   The private setting matters: your business is going in here.
3. Go to https://claude.ai/code, sign in, connect your GitHub account, and open the
   repository you just created.
4. Type `/setup`.

Important: tell readers NOT to fork the public repository for real business use, in
one plain sentence, because a fork of a public repository stays public. "Use this
template" is the private path. (Do not use the word "fork" without that explanation.)

**Self-check (both paths, its own short paragraph):** type `/` and look at the list.
If you see `setup`, `ingest`, `interview`, and `load`, you're in the right place. If
you don't, you opened the wrong folder; open the one containing `START-HERE.md`.

Keep the git-clone option as a one-line aside for people who already use git, not as
a numbered path.

Update START-HERE.md's opening so it works for both surfaces (it should not assume
local files vs web; the in-folder experience is identical). One sentence acknowledging
"whether you opened this folder on your computer or connected it on claude.ai/code"
is enough.

## F2 (P1): python3 fallback must fire on FAILURE, not just absence

`.claude/commands/ingest.md`, `.claude/commands/interview.md`, and
`.claude/skills/capture-sop/SKILL.md` gate the tool runs on `command -v python3`.
On a fresh Mac, a python3 stub exists (so the check passes) but running it fails and
pops an Apple developer-tools dialog. In all three files, change the logic to: try the
commands; if python3 is missing OR the commands fail for any reason, fall back to
rebuilding `Knowledge_Base/INDEX.md` by hand, tell the user the check was skipped, and
carry on. Never surface a raw error to the user as a dead end. Make the same
adjustment to the Python mention in `.claude/commands/load.md` and
`.claude/skills/draft/SKILL.md` ("if Python is available" -> also handle "or if the
command fails").

## F3 (P1): ingest idempotency

In `.claude/commands/ingest.md`, after the write step: offer to move the processed
source files into `_inbox/processed/` so a later `/ingest` doesn't re-read them
(default to moving; respect a no). Also add to the planning step: if a source's ideas
already exist in the knowledge base, say so and propose updating the existing file
instead of creating a near-duplicate. Update `_inbox/README.md` to mention the
`processed/` subfolder in one sentence. Confirm `.gitignore`'s `_inbox/*` pattern
still keeps `_inbox/README.md` tracked and ignores `processed/`.

## F4 (P1): Word documents and unreadable files

In `.claude/commands/ingest.md`, add to the reading step: if a file can't be read
directly (Word `.docx` is the common case), on a Mac convert it with
`textutil -convert txt -stdout <file>`; otherwise ask the user to paste the text into
the chat. Never silently skip a file: before proposing anything, list any inbox file
that couldn't be read. In `_inbox/README.md`, name what works: Word, PDF, text,
Markdown, and CSV all work; anything unreadable will be called out rather than skipped.

## F5 (P1): name where the data goes

In README.md, "Keep it private" section and the FAQ "Does my data get uploaded
anywhere?": say plainly that the content Claude reads is sent to Anthropic to generate
responses, under your own Claude account's terms and settings; the folder itself is
plain files on your computer (or in your private GitHub repository on the web path);
and 1DS Collective never sees any of it. Keep it to three sentences, no legal boilerplate.

## F6 (P2): CLAUDE.md routes through the index

In CLAUDE.md's hard rule about reading Knowledge_Base files first, add: start from
`Knowledge_Base/INDEX.md` to find them.

## F7 (P2): Windows command name

In README.md's tools section and docs/how-it-works.md: one line noting that on
Windows the command is `python` (or `py`) instead of `python3`.

## F8 (P2): permission pre-approval

Create `.claude/settings.json` containing exactly:

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 tools/index.py)",
      "Bash(python3 tools/check.py)",
      "Bash(python3 tools/selftest.py)",
      "Bash(python3 tools/find.py:*)"
    ]
  }
}
```

One sentence in docs/how-it-works.md explaining it: the folder pre-approves its own
four scripts so you aren't asked for permission every time the index rebuilds; delete
the file if you'd rather approve each run.

## F9 (P2): worked example of a filled-in CLAUDE.md

Create `docs/example-CLAUDE.md`: the CLAUDE.md brackets filled in for the fictional
Northstar Studio (consistent with the START-HERE transcript: small service companies,
clear warm direct voice, no hype). Keep the same headings as the real CLAUDE.md and
keep the unbracketed hard rules verbatim. Add a one-line pointer to it from CLAUDE.md's
top comment and from START-HERE step 1.

## New acceptance checks (in addition to PLAN.md's)

```bash
cd /Users/johnhyland/1ds-labs/AI-OS-Starter
python3 tools/selftest.py && python3 tools/index.py && python3 tools/check.py
grep -rn "claude.ai/code\|Use this template" README.md   # both present
grep -n "processed" .claude/commands/ingest.md _inbox/README.md   # present
grep -n "textutil" .claude/commands/ingest.md            # present
grep -rn "Anthropic" README.md                           # present
python3 -c "import json; json.load(open('.claude/settings.json'))"  # valid JSON
grep -rn "—" . --include="*.md" | grep -v PLAN.md | grep -v FIXES-R1.md  # zero
```

Voice rules from PLAN.md apply to every touched file. FIXES-R1.md and PLAN.md do not
ship, so they're exempt.
