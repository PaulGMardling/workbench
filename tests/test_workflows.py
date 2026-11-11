"""Static instruction contracts, not proof of agent behaviour or scheduler safety."""

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowContracts(unittest.TestCase):
    def test_creation_fetch_is_after_approval(self):
        body = (ROOT / "workflows/start-task.md").read_text()
        preflight = body.split("### 5.", 1)[1].split("### 6.", 1)[0]
        approved = body.split("### 7.", 1)[1].split("### 8.", 1)[0]
        self.assertIn("Do not fetch", preflight)
        self.assertIn("Only after explicit approval", approved)
        self.assertLess(approved.index("fetch"), approved.index("git -C"))
        self.assertIn("Revalidate", approved)

    def test_creation_guards_are_not_universal(self):
        body = (ROOT / "conventions/git-safety.md").read_text()
        universal = body.split("## Repository Validation", 1)[1].split("## Remote Safety", 1)[0]
        self.assertNotIn("does not already exist", universal)
        update = body.split("### Updating an Existing Task Branch", 1)[1].split("## Worktree Safety", 1)[0]
        self.assertIn("ancestor", update)
        self.assertIn("non-force push", update)
        self.assertIn("unavailable evidence is a blocker", update)

    def test_unavailable_consultation_and_personal_evidence_are_explicit(self):
        triage = (ROOT / "conventions/task-triage.md").read_text()
        self.assertIn("If consultation is unavailable or prohibited", triage)
        self.assertIn("If independence is an explicit requirement", triage)
        lifecycle = (ROOT / "conventions/worktree-lifecycle.md").read_text()
        self.assertIn("Personal requirements do not depend", lifecycle)
        self.assertIn("missing or unreadable", lifecycle)

    def test_publication_allowlist_keeps_private_state_out(self):
        private = [
            "config/repositories.yaml", ".local/accessibility-evidence.md",
            ".local/task-report.json", "config/github-browser.py",
            "skills/fluent-modern-migration-assessment/SKILL.md",
        ]
        public = [
            "AGENTS.md", "scripts/doctor.py", "tests/test_workflows.py",
            ".github/workflows/validate.yml", "integrations/scheduler.md",
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
