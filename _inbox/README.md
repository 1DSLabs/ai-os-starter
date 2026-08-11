# The inbox

Put source material here when you want Claude to turn it into small, labeled knowledge files.

Word documents, PDFs, text files, Markdown, and CSV files all work. Claude will call out anything it can't read instead of silently skipping it. Two or three useful documents are plenty for a first pass.

When the files are here, type `/ingest` in Claude Code. Claude will read them, propose what it plans to create, and wait for your approval before writing anything.

After a successful pass, `/ingest` can move handled sources into `_inbox/processed/` so they aren't read again.

Keep real personal data out. Remove customer and employee names, contact information, account numbers, health details, and financial details before adding a document.

This file keeps the folder present when the inbox itself is empty.
