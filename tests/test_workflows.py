"""Compatibility and publication checks, not proof of agent behaviour."""

import importlib.util
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("doctor", ROOT / "scripts/doctor.py")
doctor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(doctor)

COMPATIBILITY = {
    "conventions/task-triage.md": "workflows/agent-entry.md",
    "conventions/change-assessment.md": "workflows/agent-entry.md",
    "conventions/code-review.md": "conventions/review-protocol.md",
    "conventions/worktree-lifecycle.md": "workflows/start-task.md",
    "conventions/create-worktree.md": "workflows/start-task.md",
    "conventions/config-validation.md": "workflows/start-task.md",
}


def local_links(path):
    return {
        destination
        for target in doctor.markdown_destinations((ROOT / path).read_text())
        if (destination := doctor.local_destination(path, target)) is not None
    }


class WorkflowContracts(unittest.TestCase):
    def test_existing_entry_paths_reach_canonical_guidance(self):
        for legacy, canonical in COMPATIBILITY.items():
            with self.subTest(path=legacy):
                targets = local_links(legacy)
                self.assertIn(canonical, targets)
                self.assertFalse(targets.intersection(COMPATIBILITY))

    def test_core_guides_do_not_route_back_through_compatibility_files(self):
        canonical = set(COMPATIBILITY.values()) | {
            "AGENTS.md", "workflows/finish-task.md", "conventions/git-safety.md",
            "conventions/create-branch.md", "config/schema.md",
        }
        for path in canonical:
            with self.subTest(path=path):
                self.assertFalse(local_links(path).intersection(COMPATIBILITY))
        self.assertFalse(any(path.startswith("skills/") for path in local_links("workflows/agent-entry.md")))

    def test_publication_allowlist_keeps_private_state_out(self):
        private = [
            "config/repositories.yaml", ".local/agent-profile.md",
            ".local/accessibility-evidence.md", ".local/task-report.json",
            "config/github-browser.py",
            "skills/fluent-modern-migration-assessment/SKILL.md",
        ]
        public = [
            "AGENTS.md", "scripts/doctor.py", "tests/test_workflows.py",
            ".github/workflows/validate.yml", "integrations/scheduler.md",
            "workflows/finish-task.md",
            "skills/fluent-a11y-diagnosis/references/pr-evidence.md",
        ]
        for path in private + public:
            result = subprocess.run(
                ["git", "-C", str(ROOT), "check-ignore", "--no-index", "-q", "--", path],
                capture_output=True,
            )
            self.assertIn(result.returncode, (0, 1), result.stderr.decode())
            self.assertEqual(result.returncode, 0 if path in private else 1, path)


if __name__ == "__main__":
    unittest.main()
