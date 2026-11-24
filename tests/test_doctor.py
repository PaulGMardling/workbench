import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("doctor", ROOT / "scripts/doctor.py")
doctor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(doctor)


def config():
    return {
        "default": "sample",
        "repositories": {
            "sample": {
                "path": "/synthetic/repo", "worktreeRoot": "/synthetic/trees",
                "ide": "synthetic-editor",
                "git": {"baseRemote": "origin", "pushRemote": "origin", "baseBranch": "main"},
                "branching": {"explicitBranchRequired": True},
            }
        },
    }


class DoctorTests(unittest.TestCase):
    def errors(self, value, **kwargs):
        return doctor.config_errors(value, ROOT, **kwargs)

    def test_explicit_and_template_strategies(self):
        value = config()
        self.assertEqual(self.errors(value), [])
        value["repositories"]["sample"]["branching"] = {
            "requiresAlias": True, "templates": {"bug": "user/{alias}/fix-{description}"}
        }
        self.assertEqual(self.errors(value), [])
        value["repositories"]["sample"]["branching"]["templates"]["bug"] = "fix/{typo}"
        self.assertTrue(self.errors(value))

    def test_invalid_shapes(self):
        for value in (None, [], {"repositories": []}, {"repositories": {"sample": None}}):
            with self.subTest(value=value):
                self.assertTrue(self.errors(value))
        value = config()
        value["repositories"]["sample"]["branching"]["templates"] = {"bug": "fix/{description}"}
        self.assertTrue(self.errors(value))
        value = config()
        value["default"] = "missing"
        self.assertTrue(self.errors(value))
        self.assertTrue(self.errors(config(), repository="missing"))

    def test_unknown_fields_and_bad_paths(self):
        value = config()
        value["repositories"]["sample"]["overlasy"] = []
        self.assertTrue(self.errors(value))
        for path in ("relative/path", "$HOME/repo", ""):
            value = config()
            value["repositories"]["sample"]["path"] = path
            self.assertTrue(self.errors(value))

    def test_declared_overlays_cannot_escape(self):
        for overlay in ("/tmp/private.md", "../private.md", "notes.txt", 1):
            value = config()
            value["repositories"]["sample"]["overlays"] = [overlay]
            self.assertTrue(self.errors(value))
        value["repositories"]["sample"]["overlays"] = ["missing.md"]
        self.assertEqual(self.errors(value), [])
        self.assertTrue(self.errors(value, environment=True))

    def test_environment_git_directory_and_worktree_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            repo.mkdir()
            value = config()
            entry = value["repositories"]["sample"]
            entry.update(path=str(repo), worktreeRoot=str(root / "trees"), ide="synthetic-editor")
            with patch.object(doctor.shutil, "which", return_value="/synthetic/editor"):
                self.assertTrue(self.errors(value, environment=True))
                (repo / ".git").mkdir()
                self.assertEqual(self.errors(value, environment=True), [])
                (repo / ".git").rmdir()
                (repo / ".git").write_text("gitdir: /synthetic/metadata")
                self.assertEqual(self.errors(value, environment=True), [])
            with patch.object(doctor.shutil, "which", return_value=None):
                self.assertTrue(self.errors(value, environment=True))

    def test_editor_override_precedence(self):
        value = config()
        value["copilotApp"] = {"ide": "app-editor"}
        with patch.object(doctor.shutil, "which", return_value="/synthetic/editor") as which:
            self.errors(value, environment=True, host="copilot", editor="explicit-editor")
            which.assert_called_once_with("explicit-editor")

    def test_duplicate_and_malformed_yaml_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            for body in ("repositories: {}\nrepositories: {}\n", "repositories: ["):
                path.write_text(body)
                with self.assertRaises(ValueError):
                    doctor.load_config(path)

    def test_content_check_ignores_local_files_but_catches_public_leaks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "readme.md").write_text("[missing](missing.md)\n")
            (root / "private.md").write_text("private local data")
            result = type("Result", (), {"returncode": 0, "stdout": b"readme.md\0"})()
            permitted = type("Result", (), {"returncode": 1, "stdout": b""})()
            def command_result(command, **kwargs):
                return permitted if "check-ignore" in command else result
            with patch.object(doctor.subprocess, "run", side_effect=command_result):
                self.assertTrue(doctor.content_errors(root))
                (root / "readme.md").write_text("Portable guidance\n")
                self.assertEqual(doctor.content_errors(root), [])
                (root / "readme.md").write_text("ghp_" + "x" * 24)
                self.assertTrue(doctor.content_errors(root))

    def test_force_tracked_private_file_is_rejected(self):
        listed = type("Result", (), {"returncode": 0, "stdout": b"config/repositories.yaml\0"})()
        ignored = type("Result", (), {"returncode": 0, "stdout": b"config/repositories.yaml\0"})()
        with patch.object(doctor.subprocess, "run", side_effect=[listed, ignored]):
            self.assertTrue(any("publication allowlist" in error for error in doctor.content_errors(ROOT)))

    def content_errors(self, body, source="readme.md"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            published = {source, "guide.md", "docs/with space.md"}
            for name in published:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body if name == source else "Published document\n")
            listed = type("Result", (), {"returncode": 0, "stdout": "\0".join(published).encode()})()
            permitted = type("Result", (), {"returncode": 1, "stdout": b""})()
            with patch.object(doctor.subprocess, "run", side_effect=[listed, permitted]):
                return doctor.content_errors(root)

    def test_markdown_titles_references_and_images(self):
        for body in (
            '[Guide](guide.md "Introduction")',
            "[Guide][g]\n\n[g]: guide.md 'Introduction'",
            "[Guide][]\n\n[Guide]: guide.md",
            "[Guide]\n\n[Guide]: guide.md",
            "![Example][image]\n\n[image]: guide.md",
        ):
            with self.subTest(body=body):
                self.assertEqual(self.content_errors(body), [])
        for body in ("[Missing][g]\n\n[g]: missing.md", "![Missing](missing.md)"):
            with self.subTest(body=body):
                self.assertTrue(self.content_errors(body))

    def test_uri_fragments_queries_and_encoded_paths(self):
        for body in (
            "[Contact](mailto:team@example.invalid)",
            "[Phone](tel:+123)",
            "[Web](https://example.invalid/guide)",
            "[Web](//example.invalid/guide)",
            "[Here](#section)",
            "[Here](?plain=1#section)",
            "[Guide](guide.md?plain=1#section)",
            "[Spaces](docs/with%20space.md)",
            "[Spaces](<docs/with space.md>)",
        ):
            with self.subTest(body=body):
                self.assertEqual(self.content_errors(body), [])
        self.assertEqual(self.content_errors("[Guide](../guide.md)", "docs/readme.md"), [])

    def test_examples_are_not_rendered_links(self):
        self.assertEqual(self.content_errors(
            '`[Example](missing.md)`\n\n```md\n[Example](missing.md)\n```\n'
        ), [])

    def test_html_links_and_images_are_checked(self):
        for body in ('<a href="guide.md">Guide</a>', '<img src="guide.md" />'):
            with self.subTest(body=body):
                self.assertEqual(self.content_errors(body), [])
        for body in ('<a href="missing.md">Missing</a>', '<img src="missing.md">'):
            with self.subTest(body=body):
                self.assertTrue(self.content_errors(body))
        self.assertEqual(self.content_errors('<!-- <a href="missing.md">Example</a> -->'), [])

    def test_link_paths_cannot_bypass_publication_boundary(self):
        for target in (
            ".local/private.md", "../guide.md", "/guide.md", "%2Fguide.md",
            "%2e%2e/guide.md", "docs/%2e%2e/%2e%2e/guide.md", "docs/%00.md",
            "docs/%5cguide.md", "file:///guide.md", "javascript:alert(1)",
        ):
            with self.subTest(target=target):
                self.assertTrue(self.content_errors(f'<a href="{target}">Link</a>'))

    def test_missing_markdown_dependency_is_reported(self):
        with patch.object(doctor, "MarkdownIt", None):
            self.assertTrue(any("markdown-it-py is missing" in error for error in doctor.content_errors(ROOT)))

    def test_overlay_symlink_loop_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "loop.md").symlink_to("loop.md")
            value = config()
            value["repositories"]["sample"]["overlays"] = ["loop.md"]
            errors = doctor.config_errors(value, root)
            self.assertTrue(any("cannot be resolved" in error for error in errors))

    def test_cli_checks_actual_git_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "--template=", "-q", str(root)], check=True)
            (root / "config").mkdir()
            (root / "config/repositories.example.yaml").write_text(
                (ROOT / "config/repositories.example.yaml").read_text()
            )
            (root / ".gitignore").write_text(".local/\n")
            (root / ".local").mkdir()
            (root / ".local/private.md").write_text("ghp_" + "x" * 24)
            (root / "guide.md").write_text("Published\n")
            document = root / "readme.md"
            command = [sys.executable, str(ROOT / "scripts/doctor.py"), "--root", str(root)]
            document.write_text('[Guide](guide.md "Introduction")\n[Contact](mailto:team@example.invalid)\n')
            valid = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(valid.returncode, 0, valid.stderr)
            for body in ("[Missing][g]\n\n[g]: missing.md", "[Private](.local/private.md)"):
                document.write_text(body)
                invalid = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(invalid.returncode, 1, invalid.stdout)
                self.assertIn("local Markdown link", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
