import importlib.util
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
