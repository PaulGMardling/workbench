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
            "workflows/finish-task.md",
        ]
        for path in private + public:
            result = subprocess.run(
                ["git", "-C", str(ROOT), "check-ignore", "--no-index", "-q", "--", path],
                capture_output=True,
            )
            self.assertIn(result.returncode, (0, 1), result.stderr.decode())
            self.assertEqual(result.returncode, 0 if path in private else 1, path)

    def test_delivery_is_loaded_before_implementation_with_opt_out_boundaries(self):
        entry = (ROOT / "workflows/agent-entry.md").read_text()
        route = next(line for line in entry.splitlines() if line.startswith("| Planning or implementation |"))
        self.assertIn("finish-task.md", route)
        delivery = (ROOT / "workflows/finish-task.md").read_text()
        for boundary in (
            "Delivery is opt-out", "Creating a PR is opt-in",
            "not review, diagnosis", "host's permissions",
            "pre-existing staged content", "actual checked-out branch",
            "explicit publishing refspec", "closed/merged PR",
            "concurrent edits", "single versioned block", "partial delivery",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, delivery)
        lifecycle = (ROOT / "conventions/worktree-lifecycle.md").read_text()
        self.assertIn("sole exception is the exact revision field", lifecycle)
        safety = (ROOT / "conventions/git-safety.md").read_text()
        self.assertIn("per-operation rule applies to the protected actions above", safety)


if __name__ == "__main__":
    unittest.main()
