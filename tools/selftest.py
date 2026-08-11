#!/usr/bin/env python3
"""Run the knowledge-tool tests with Python's standard library.

From the repository root or this directory, run:

    python3 tools/selftest.py
    python3 selftest.py
"""

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent

sys.path.insert(0, str(TOOLS_DIR))

import check as check_tool  # noqa: E402
import find as find_tool  # noqa: E402
import index as index_tool  # noqa: E402
import kb  # noqa: E402
from frontmatter import LabelBlockError, parse  # noqa: E402


def knowledge_text(
    entry_id="sample-entry",
    title="Sample Entry",
    file_type="principle",
    summary="A short summary for the test file.",
    updated="2026-08-11",
    extra_labels=None,
    body="Test body.\n",
):
    """Return a complete knowledge file for a temporary test folder."""
    labels = [
        "---",
        "id: %s" % entry_id,
        "title: %s" % title,
        "type: %s" % file_type,
        "summary: %s" % summary,
        "updated: %s" % updated,
    ]
    labels.extend(extra_labels or [])
    labels.extend(["---", "", body])
    return "\n".join(labels)


def write_knowledge(kb_root, folder, filename, **values):
    """Write one temporary knowledge file and return its path."""
    target_dir = Path(kb_root, folder)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / filename
    target.write_text(knowledge_text(**values), encoding="utf-8")
    return target


class FrontmatterTests(unittest.TestCase):
    def test_crlf(self):
        text = (
            "---\r\n"
            "id: windows-lines\r\n"
            "title: Windows Lines\r\n"
            "updated: 2026-08-11\r\n"
            "---\r\n"
            "Body\r\n"
        )
        labels = parse(text)
        self.assertEqual(labels["id"], "windows-lines")
        self.assertEqual(labels["updated"], "2026-08-11")

    def test_smart_quotes(self):
        labels = parse(
            "---\n"
            "title: “A Friendly Voice”\n"
            "aliases: [‘Friendly’, “Warm”]\n"
            "---\n"
        )
        self.assertEqual(labels["title"], "A Friendly Voice")
        self.assertEqual(labels["aliases"], ["Friendly", "Warm"])

    def test_colons_stay_in_values(self):
        labels = parse(
            "---\n"
            "summary: Open from 9:00 to 5:00\n"
            "source: https://example.com:8443/reference\n"
            "---\n"
        )
        self.assertEqual(labels["summary"], "Open from 9:00 to 5:00")
        self.assertEqual(labels["source"], "https://example.com:8443/reference")

    def test_tab_indented_list(self):
        labels = parse(
            "---\n"
            "tags:\n"
            "\t- planning\n"
            "\t- delivery\n"
            "---\n"
        )
        self.assertEqual(labels["tags"], ["planning", "delivery"])

    def test_inline_list(self):
        labels = parse(
            "---\n"
            "tags: [planning, 'client work', delivery]\n"
            "---\n"
        )
        self.assertEqual(labels["tags"], ["planning", "client work", "delivery"])

    def test_utf8_bom(self):
        labels = parse("\ufeff---\nid: bom-file\n---\n")
        self.assertEqual(labels, {"id": "bom-file"})

    def test_no_block(self):
        self.assertIsNone(parse("# A normal Markdown file\n\nNo labels here.\n"))

    def test_missing_colon_has_clear_error(self):
        with self.assertRaisesRegex(LabelBlockError, "missing a colon"):
            parse("---\nid broken-entry\n---\n")

    def test_scalar_values_stay_strings(self):
        labels = parse("---\nupdated: 2026-08-11\nowner: Yes\n---\n")
        self.assertEqual(labels["updated"], "2026-08-11")
        self.assertEqual(labels["owner"], "Yes")


class KnowledgeHelperTests(unittest.TestCase):
    def test_file_iterator_skips_generated_and_readme_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_root = Path(temp_dir, "Knowledge_Base")
            write_knowledge(kb_root, "principles", "keep.md")
            Path(kb_root, "INDEX.md").write_text("generated", encoding="utf-8")
            Path(kb_root, "principles", "_README.md").write_text(
                "guide", encoding="utf-8"
            )

            found = [Path(path).name for path in kb.iter_knowledge_files(str(kb_root))]

        self.assertEqual(found, ["keep.md"])


class IndexTests(unittest.TestCase):
    def test_builds_markdown_and_json_indexes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_root = Path(temp_dir, "Knowledge_Base")
            write_knowledge(
                kb_root,
                "principles",
                "clear-writing.md",
                entry_id="clear-writing",
                title="Clear Writing",
                summary="How the team writes for customers.",
            )

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = index_tool.main(["index.py", str(kb_root)])

            self.assertEqual(result, 0)
            index_path = kb_root / "INDEX.md"
            map_path = kb_root / "_index.json"
            self.assertTrue(index_path.is_file())
            self.assertTrue(map_path.is_file())
            self.assertIn(
                "[Clear Writing](principles/clear-writing.md)",
                index_path.read_text(encoding="utf-8"),
            )
            payload = json.loads(map_path.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["files"], {"clear-writing": "principles/clear-writing.md"}
            )
            self.assertIn("Indexed 1 file.", output.getvalue())

    def test_duplicate_ids_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_root = Path(temp_dir, "Knowledge_Base")
            write_knowledge(
                kb_root,
                "principles",
                "first.md",
                entry_id="shared-id",
                title="First File",
            )
            write_knowledge(
                kb_root,
                "principles",
                "second.md",
                entry_id="shared-id",
                title="Second File",
            )

            entries, problems = index_tool.build(str(kb_root))

            self.assertEqual(len(entries), 1)
            self.assertEqual(len(problems), 1)
            self.assertIn("two files share the id 'shared-id'", problems[0])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = index_tool.main(["index.py", str(kb_root)])
            self.assertEqual(result, 1)
            self.assertIn("1 file need attention", output.getvalue())


class CheckTests(unittest.TestCase):
    def test_missing_required_fields_are_problems(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_root = Path(temp_dir, "Knowledge_Base")
            target_dir = kb_root / "principles"
            target_dir.mkdir(parents=True)
            target = target_dir / "incomplete.md"
            target.write_text(
                "---\nid: incomplete\ntype: principle\n---\n\nBody.\n",
                encoding="utf-8",
            )

            problems, suggestions, entry_id = check_tool.check_file(
                str(kb_root), str(target)
            )

        self.assertEqual(suggestions, [])
        self.assertEqual(entry_id, "incomplete")
        self.assertTrue(any("missing `title`" in problem for problem in problems))
        self.assertTrue(any("missing `summary`" in problem for problem in problems))
        self.assertTrue(any("missing `updated`" in problem for problem in problems))

    def test_wrong_folder_is_a_problem(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_root = Path(temp_dir, "Knowledge_Base")
            target = write_knowledge(
                kb_root,
                "principles",
                "project-kickoff.md",
                entry_id="project-kickoff",
                title="Project Kickoff",
                file_type="playbook",
            )

            problems, _, _ = check_tool.check_file(str(kb_root), str(target))

        self.assertTrue(any("which holds `principle` files" in p for p in problems))
        self.assertTrue(any("its type is `playbook`" in p for p in problems))

    def test_shipped_examples_pass(self):
        kb_root = REPO_ROOT / "Knowledge_Base"
        expected = {
            "EXAMPLE-how-we-write.md",
            "EXAMPLE-new-client-onboarding.md",
            "EXAMPLE-project-kickoff-email.md",
            "EXAMPLE-refund-requests.md",
        }
        examples = sorted(kb_root.glob("*/EXAMPLE-*.md"))

        self.assertEqual({path.name for path in examples}, expected)
        for path in examples:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                problems, _, _ = check_tool.check_file(str(kb_root), str(path))
                self.assertEqual(problems, [])


class FindTests(unittest.TestCase):
    def test_exact_title_ranks_first_and_cli_returns_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_root = Path(temp_dir, "Knowledge_Base")
            write_knowledge(
                kb_root,
                "decisions",
                "refund-requests.md",
                entry_id="refund-requests",
                title="Refund Requests",
                file_type="decision",
                summary="When the business approves a refund.",
                extra_labels=["tags: [refund, requests]"],
            )
            write_knowledge(
                kb_root,
                "records",
                "customer-credit.md",
                entry_id="customer-credit",
                title="Customer Credit",
                file_type="record",
                summary="A record that mentions refund requests.",
                body="A refund request appears here too.\n",
            )

            entries = find_tool.load_files(str(kb_root))
            results = find_tool.search("Refund Requests", entries)
            self.assertEqual(results[0]["id"], "refund-requests")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(TOOLS_DIR / "find.py"),
                    "Refund Requests",
                    "--json",
                ],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["query"], "Refund Requests")
        self.assertEqual(payload["results"][0]["id"], "refund-requests")
        self.assertIsInstance(payload["results"][0]["score"], int)


if __name__ == "__main__":
    unittest.main(verbosity=2)
