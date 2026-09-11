import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time
import unittest

PACK = Path(__file__).resolve().parents[1]
CLI = PACK / "bin/erixpo"
RUNTIME_SPEC = importlib.util.spec_from_file_location("erixpo_runtime", PACK / "scripts/erixpo-runtime.py")
RUNTIME = importlib.util.module_from_spec(RUNTIME_SPEC)
RUNTIME_SPEC.loader.exec_module(RUNTIME)


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="erixpo runtime ")
        self.root = Path(self.tmp.name)
        (self.root / ".erixpo").mkdir()
        (self.root / "README.md").write_text("fixture")
        (self.root / ".erixpo/stack.md").write_text("check: test -f README.md\n")
        self.plan = self.root / ".erixpo/plan.md"
        self.plan.write_text("status: approved\n- [ ] First\n- [ ] Second\n")
        self.env = dict(os.environ, ERIXPO_WORKER_CMD="exit 0")

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, *args, **kw):
        return subprocess.run(["bash", str(CLI), "--root", str(self.root), *args], env=self.env, cwd=PACK, capture_output=True, text=True, timeout=15, **kw)

    def run_worker(self, command, *extra):
        self.env["ERIXPO_WORKER_CMD"] = command
        return self.call("run", "--worker", "generic", "--no-isolate", "--max", "4", *extra)

    def state(self):
        return (self.root / ".erixpo/state.md").read_text()

    def render_prompt(self, run_id="run-test"):
        RUNTIME.prompt(self.root.resolve(), self.plan.resolve(), 1, "generic", {}, run_id)
        return (self.root / ".erixpo/loop-prompt.md").read_text()

    def test_prompt_contains_only_current_slice_body(self):
        self.plan.write_text(
            "status: approved\n"
            "## Non-goals\n"
            "- SHARED-NON-GOAL\n"
            "## UI\n"
            "- SHARED-UI-CONSTRAINT\n"
            "## Slices\n"
            "### Current slice\n"
            "- Acceptance: CURRENT-ACCEPTANCE\n"
            "- Edges: CURRENT-EDGES\n"
            "- Check: test -f current\n"
            "- Status: todo\n"
            "### Unrelated slice\n"
            "- Acceptance: UNRELATED-ACCEPTANCE\n"
            "- Edges: UNRELATED-EDGES\n"
            "- Check: test -f unrelated\n"
            "- Status: todo\n"
        )
        (self.root / ".erixpo/classify.md").write_text("CLASSIFY-SENTINEL")
        (self.root / ".erixpo/USER.md").write_text("USER-SENTINEL")
        (self.root / ".erixpo/lessons.md").write_text("LESSONS-SENTINEL")
        prompt = self.render_prompt()
        for sentinel in ("SHARED-NON-GOAL", "SHARED-UI-CONSTRAINT", "CURRENT-ACCEPTANCE", "CURRENT-EDGES", "test -f current", "Status: todo"):
            self.assertIn(sentinel, prompt)
        for sentinel in ("UNRELATED-ACCEPTANCE", "UNRELATED-EDGES", "test -f unrelated", "CLASSIFY-SENTINEL", "USER-SENTINEL", "LESSONS-SENTINEL"):
            self.assertNotIn(sentinel, prompt)

    def test_prompt_checkbox_plan_keeps_complete_list(self):
        self.plan.write_text(
            "status: approved\n"
            "- [ ] First checkbox acceptance\n"
            "  Edge: first checkbox edge\n"
            "- [x] Second checkbox acceptance\n"
        )
        prompt = self.render_prompt()
        for sentinel in ("First checkbox acceptance", "first checkbox edge", "Second checkbox acceptance"):
            self.assertIn(sentinel, prompt)

    def test_prompt_checkbox_plan_with_heading_keeps_checkbox_context(self):
        self.plan.write_text(
            "status: approved\n"
            "## Notes\n"
            "### Context only\n"
            "- [ ] First checkbox acceptance\n"
        )
        prompt = self.render_prompt()
        self.assertIn("First checkbox acceptance", prompt)
        self.assertNotIn("No incomplete slice remains", prompt)

    def test_prompt_reports_failed_verification_for_all_done_plan(self):
        self.plan.write_text(
            "status: complete\n"
            "### Finished slice\n"
            "- Acceptance: finished\n"
            "- Check: test -f result\n"
            "- Status: done\n"
        )
        log = self.root / ".erixpo/failed-check.log"
        (self.root / ".erixpo/verification.json").write_text(json.dumps({
            "run_id": "run-test",
            "plan": str(self.plan),
            "checks": [{"command": "python3 verify.py", "exit_code": 7, "log": str(log)}]
        }))
        prompt = self.render_prompt()
        self.assertIn("Repair previous verification", prompt)
        self.assertIn("python3 verify.py", prompt)
        self.assertIn("exit 7", prompt)
        self.assertIn(str(log), prompt)
        self.assertIn("do not declare completion", prompt)
        self.assertNotIn("plan complete", prompt.lower())

    def test_prompt_ignores_stale_verification_receipts(self):
        other_plan = self.root / ".erixpo/other-plan.md"
        for receipt in (
            {"run_id": "old-run", "plan": str(self.plan)},
            {"run_id": "run-test", "plan": str(other_plan)},
        ):
            receipt["checks"] = [{"command": "stale-check", "exit_code": 9, "log": "stale.log"}]
            (self.root / ".erixpo/verification.json").write_text(json.dumps(receipt))
            self.assertNotIn("stale-check", self.render_prompt())

    def test_root_and_subcommand_flags(self):
        self.assertEqual(self.call("check").returncode, 0)
        out = self.call("research-scope", "--class", "new")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.strip(), "full")

    def test_failed_worker_never_completes_green_plan(self):
        out = self.run_worker("exit 7")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("worker_failed", self.state())
        self.assertIn("iteration: 3", self.state())

    def test_two_slices_continue_after_first_green_check(self):
        worker = self.root / "worker.py"
        worker.write_text("from pathlib import Path\np=Path('.erixpo/plan.md')\np.write_text(p.read_text().replace('[ ]', '[x]', 1))\n")
        out = self.run_worker("python3 worker.py")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("iteration: 2", self.state())
        self.assertIn("plan_complete", self.state())
        receipt = json.loads((self.root / ".erixpo/verification.json").read_text())
        self.assertEqual(receipt["checks"][0]["exit_code"], 0)

    def test_runtime_events_are_searchable(self):
        self.plan.write_text("status: approved\n- [x] First\n")
        self.assertEqual(self.run_worker("exit 0").returncode, 0)
        out = self.call("search", "--kind", "sessions")
        self.assertIn("Prior session: run-", out.stdout)

    def test_state_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            target = self.root / ".erixpo/state.md"
            target.symlink_to(Path(outside) / "state.md")
            out = self.run_worker("exit 0")
            self.assertNotEqual(out.returncode, 0)
            self.assertFalse((Path(outside) / "state.md").exists())

    def test_background_process_is_terminated(self):
        child = self.root / "child.py"
        child.write_text("from pathlib import Path\nimport time\nPath('child.ready').touch()\ntime.sleep(.6)\nPath('leaked').touch()\n")
        worker = self.root / "worker.py"
        worker.write_text("import subprocess,time\nfrom pathlib import Path\nsubprocess.Popen(['python3','child.py'])\nwhile not Path('child.ready').exists(): time.sleep(.01)\n")
        self.run_worker("python3 worker.py", "--max", "1")
        time.sleep(.7)
        self.assertFalse((self.root / "leaked").exists(), "background descendant survived the worker")

    def test_installed_isolated_run_review_close_and_recall(self):
        def git(*args):
            subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)
        git("init", "-b", "main")
        git("config", "user.name", "Test")
        git("config", "user.email", "test@example.invalid")
        git("add", "README.md")
        git("commit", "-m", "fixture")
        subprocess.run(["bash", str(PACK / "install.sh"), "--target", str(self.root), "--host", "generic"], check=True, capture_output=True)
        (self.root / ".erixpo/stack.md").write_text("check: test -f result.txt\n")
        (self.root / ".erixpo/worker.py").write_text("from pathlib import Path\nimport subprocess\np=Path('.erixpo/plan.md')\np.write_text(p.read_text().replace('[ ]','[x]'))\nPath('result.txt').write_text('verified result')\nPath('.erixpo/USER.md').write_text('autonomy: plan-then-go\\n')\nsubprocess.run(['git','add','result.txt'],check=True)\nsubprocess.run(['git','commit','-m','result'],check=True)\n")
        self.env["ERIXPO_WORKER_CMD"] = "python3 .erixpo/worker.py"
        cli = self.root / ".erixpo/bin/erixpo"
        def installed(*args, root=None):
            return subprocess.run([str(cli), "--root", str(root or self.root), *args], capture_output=True, text=True, env=self.env, timeout=15)
        out = installed("run", "--worker", "generic", "--max", "2")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        row = json.loads((self.root / ".erixpo/worktrees.jsonl").read_text().splitlines()[-1])
        child = Path(row["path"])
        try:
            result = installed("review", "--stage", "1", root=child)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            evidence = json.loads((child / ".erixpo/REVIEW-stage1.json").read_text())
            (child / ".erixpo/REVIEW.md").write_text(f"Result: ship\nReview-ID: {evidence['review_id']}\nReviewer: independent-fixture\n")
            result = installed("close", "--id", row["id"])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(child.exists())
            self.assertEqual((self.root / "result.txt").read_text(), "verified result")
            self.assertIn("Prior session: run-", installed("search", "--kind", "sessions").stdout)
        finally:
            if child.exists():
                subprocess.run(["git", "-C", str(self.root), "worktree", "remove", "--force", str(child)], capture_output=True)

    def test_green_no_progress_stops(self):
        out = self.run_worker("exit 0")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("no_progress", self.state())

    def test_repeated_check_failure_stops(self):
        (self.root / ".erixpo/stack.md").write_text("check: test -f missing\n")
        out = self.run_worker("exit 0")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("check_failed", self.state())
        self.assertIn("iteration: 3", self.state())

    def test_draft_and_missing_worker_fail_before_isolation(self):
        self.plan.write_text("status: draft\n- [ ] First\n")
        out = self.call("run", "--worker", "generic")
        self.assertIn("approved", out.stderr)
        self.assertFalse((self.root / ".erixpo/worktrees.jsonl").exists())
        self.plan.write_text("status: approved\n- [ ] First\n")
        out = self.call("run", "--worker", "not-a-worker")
        self.assertIn("unsupported worker", out.stderr)
        self.assertFalse((self.root / ".erixpo/worktrees.jsonl").exists())

    def test_budget_file_and_invalid_arguments(self):
        (self.root / ".erixpo/budget.md").write_text("max_iterations: 1\nmax_seconds: 10\n")
        out = self.call("run", "--worker", "generic", "--no-isolate")
        self.assertEqual(out.returncode, 2)
        self.assertIn("budget_exhausted", self.state())
        self.assertNotEqual(self.call("run", "--max").returncode, 0)
        self.assertNotEqual(self.call("run", "--timeout", "0").returncode, 0)

    def test_timeout(self):
        out = self.run_worker("sleep 30", "--timeout", "1")
        self.assertEqual(out.returncode, 2)
        self.assertIn("budget_exhausted", self.state())

    def test_sigterm_propagates_and_records_outcome(self):
        self.env["ERIXPO_WORKER_CMD"] = "sleep 30"
        with subprocess.Popen(["bash", str(CLI), "--root", str(self.root), "run", "--worker", "generic", "--no-isolate"], env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            deadline = time.monotonic() + 5
            while not list((self.root / ".erixpo").glob("*-worker.log")) and time.monotonic() < deadline:
                time.sleep(.02)
            proc.send_signal(signal.SIGTERM)
            out, err = proc.communicate(timeout=5)
            self.assertEqual(proc.returncode, 143, out + err)
        self.assertIn("interrupted", self.state())

    def test_deleted_slice_is_not_completion(self):
        worker = self.root / "worker.py"
        worker.write_text("from pathlib import Path\nPath('.erixpo/plan.md').write_text('status: approved\\n- [x] First\\n')\n")
        out = self.run_worker("python3 worker.py")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("changed approved slice", out.stderr)

    def test_slice_checks_and_legacy_state_migration(self):
        self.plan.write_text("status: approved\n### 1. First\n- Check: test -f result.txt\n- Status: todo\n")
        (self.root / ".erixpo/state.yaml").write_text("phase: approved\nceremony: light\n")
        worker = self.root / "worker.py"
        worker.write_text("from pathlib import Path\np=Path('.erixpo/plan.md')\np.write_text(p.read_text().replace('Status: todo','Status: done'))\nPath('result.txt').write_text('done')\n")
        out = self.run_worker("python3 worker.py")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("ceremony: light", self.state())
        self.assertEqual((self.root / ".erixpo/state.yaml").read_text(), "phase: approved\nceremony: light\n")
        receipt = json.loads((self.root / ".erixpo/verification.json").read_text())
        self.assertEqual(len(receipt["checks"]), 2)


class RoutingTests(unittest.TestCase):
    def test_platform_and_intent(self):
        spec = importlib.util.spec_from_file_location("classify", PACK / "scripts/classify-signals.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for sentence, expected in [("/erixpo new", "new"), ("update the README", "docs"), ("add an error handler", "feature")]:
            self.assertEqual(module.classify(sentence)["request_class"], expected)
        self.assertEqual(module.classify("I want a macOS SwiftUI app")["surface"], "macos")
