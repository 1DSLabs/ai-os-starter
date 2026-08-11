# FIX ROUND 2 (Codex review findings, boss-dispositioned; implement all)

Apply on top of round 1. PLAN.md voice and quality rules still bind. FIXES-R1.md,
FIXES-R2.md, and PLAN.md do not ship and are exempt from voice checks.

## G1 (P1): example files must never masquerade as business truth

- `tools/index.py`: when a file's labels include `status: example`, render its Name
  cell as `Title (example)` in INDEX.md. Add a selftest case.
- Add one line to `.claude/commands/load.md`, `.claude/skills/draft/SKILL.md`, and
  `.claude/skills/capture-sop/SKILL.md`: files marked `status: example` show the
  format only; never treat them as real policy, coverage, or an update target. If an
  example is the only match for a real question, say no real file covers it yet and
  offer to create one.
- Regenerate INDEX.md and `_index.json` afterward.

## G2 (P1): approval before writing, and no self-triggered mutations

- `.claude/skills/capture-sop/SKILL.md`: before creating the playbook file, show the
  draft (or a faithful summary of it) and get a clear yes. No file writes before that yes.
- Add `disable-model-invocation: true` to the frontmatter of
  `.claude/commands/setup.md`, `.claude/commands/ingest.md`, and
  `.claude/commands/interview.md` (the three that write files; `/load` stays as is).

## G3 (P1): web-path persistence and pasted material

- README.md Path B: add one sentence at the end: when a browser session ends, tell
  Claude to commit and push the work so it's saved to the repository.
- `.claude/commands/ingest.md`: if `_inbox/` has no source files but the user pasted
  material into the chat (common in the browser), ingest the pasted material through
  the same propose-approve-write flow.

## G4 (P1): sensitive originals left in _inbox

`.claude/commands/ingest.md`, final report step: when sources contained personal
details, remind the user that the original files in `_inbox/` still hold them, and
offer to help clean or remove those originals. Never delete without a clear yes.

## G5 (P1): update FAQ must protect custom skills

README.md "How do I update" FAQ: the keep-safe list must also name any skills and
commands the user created under `.claude/`.

## G6 (P1): tools robustness (all in tools/, with selftest coverage for each)

- `frontmatter.py`: a duplicated key raises LabelBlockError naming the key and line.
  A list following a scalar value on the same key raises a clear error. An opening
  `---` with no closing `---` raises a clear error instead of parsing as "no block".
  A list value where a string is expected must never raw-TypeError downstream:
  `check.py` reports "id must be a single value, not a list" style problems.
- `check.py`: validate `updated` is a real YYYY-MM-DD calendar date; report otherwise.
- `index.py`: build both artifacts fully in memory, then write each via a temp file
  in the same directory and `os.replace`, so a crash can't leave a half-written index.
  URL-encode link targets (spaces and `#` in user filenames). Count and report files
  skipped for having no label block or no id: "Indexed N files, skipped M without
  labels: <paths>" (only when M > 0).
- `kb.py`: pass an `onerror` handler to `os.walk` that collects unreadable paths;
  report them as problems in check.py rather than skipping silently. Match `.md`
  case-insensitively.
- `find.py`: tokenization becomes Unicode-aware (casefold; word chars via `\w` with
  re.UNICODE) so non-Latin content is searchable. Reject `--top` values below 1 with
  a plain usage message.
- `selftest.py`: the shipped-examples test must skip cleanly (not fail) when no
  example files exist, since users are told to delete them. Add cases for: duplicate
  key error, unterminated block error, list-valued id reported by check, bad calendar
  date reported, unicode title found by find, `(example)` marker in INDEX.md.

## G7 (P2): wording sweep

- README.md tools section: replace the "no installs" framing with "The scripts need
  no extra packages." Keep the Windows `python` note from round 1.
- README.md command-vs-skill FAQ: both are packaged instructions; a command is
  something you type deliberately (`/ingest`), a skill is a method Claude can also
  pick up on its own when a task fits. Drop any claim about underlying mechanisms.
- CLAUDE.md hard rule: broaden "process, rule, term, or prior decision" to also
  cover how the business sounds (voice, templates). Keep it one sentence.
- `.claude/commands/load.md`: define stale in passing: "stale means the index no
  longer matches the files actually in the folders". Keep the search phrase to plain
  words (letters, numbers, spaces).
- START-HERE.md "As you grow": prescribe the supported nesting shape explicitly:
  keep the type folder first, then a brand or location subfolder, e.g.
  `Knowledge_Base/playbooks/brand-a/`. The tools already handle nesting; say so.
- `docs/file-format.md`: the label-block requirement applies to knowledge files you
  create; generated files (INDEX.md, _index.json) and the folder `_README.md` guides
  don't carry one.
- `docs/file-format.md` + `Knowledge_Base/models/_README.md` + README table: models
  include calculations (align with ingest.md's wording).
- `docs/skill-format.md` and skill-template: "Keep the frontmatter to `name` and
  `description` unless you know you need more."
- Windows prerequisite, README "Before you start": one conditional line, "If Claude
  Code on Windows asks for Git, install Git for Windows from git-scm.com."
- ingest/interview/capture-sop check step: fix problems caused by the new files;
  report pre-existing problems without touching unrelated files unless asked.
- Python check wording in commands: "Check for Python 3 (`python3`, or `python`/`py`
  on Windows)."

## Acceptance

Re-run everything from PLAN.md and FIXES-R1.md, plus:

```bash
cd /Users/johnhyland/1ds-labs/AI-OS-Starter
python3 tools/selftest.py                       # all pass, incl. new cases
python3 tools/index.py && python3 tools/check.py
grep -n "(example)" Knowledge_Base/INDEX.md      # 4 hits
grep -n "disable-model-invocation" .claude/commands/*.md | wc -l   # 3
grep -rn "—" . --include="*.md" | grep -v -e PLAN.md -e FIXES      # zero
```

Then remove any temporary artifacts you created. Do not touch git.
