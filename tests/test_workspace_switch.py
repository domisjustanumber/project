"""Branch selection checks with mocked Git; never mutate repository state."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_workspace as fixtures

module = fixtures.module


class SwitchTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.root.joinpath("repos.toml").write_text('''core = "core"
[[repos]]
name = "core"
path = "core"
url = "https://example.com/core"
branch = "old"
[[repos]]
name = "dep"
path = "dep"
source = "dep"
[[repos]]
name = "utility"
path = "utility"
source = "utility"
''')
        self.workspace = module.Workspace(self.root)
        self.sources = '''[tool.uv.sources]
dep = {git = "https://example.com/dep", branch = "dependency-release"}
utility = {git = "https://example.com/utility"}
'''
        self.calls = []
        self.dirty = None
        self.missing = set()
        self.occupied = False
        self.fail_switch = None
        self.git_patch = patch.object(module, "git", side_effect=self.git)
        self.git_patch.start()
        self.addCleanup(self.git_patch.stop)
        verify = patch.object(self.workspace, "verify")
        verify.start()
        self.addCleanup(verify.stop)

    def git(self, path, *args):
        self.calls.append((path.name, args))
        if args[0] == "rev-parse":
            return str(path / ".git" / args[-1])
        if args[0] == "status":
            return " M user-work" if path.name == self.dirty else ""
        if args[0] == "branch":
            return "old"
        if args[0] == "show-ref":
            if (path.name, args[-1]) in self.missing:
                raise ValueError("missing ref")
            return "sha"
        if args[0] == "show":
            return self.sources
        if args[0] == "worktree":
            return "branch refs/heads/dependency-release" if self.occupied and path.name == "dep" else ""
        if args[0] == "switch" and path.name == self.fail_switch:
            raise ValueError("file conflict")
        return ""

    def run_switch(self, dry_run=False):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return self.workspace.switch("conference", dry_run)

    def mutations(self):
        return [(name, args) for name, args in self.calls if args[0] in
                {"switch", "fetch", "pull", "merge", "restore", "reset"}]

    def test_preview_reads_selected_core_and_does_not_mutate(self):
        self.assertEqual(self.run_switch(True), 0)
        self.assertIn(("core", ("show", "refs/heads/conference:pyproject.toml")), self.calls)
        self.assertIn(("dep", ("check-ref-format", "--branch", "dependency-release")), self.calls)
        self.assertFalse(self.mutations())
        self.assertFalse(any(name == "utility" for name, _ in self.calls))

    def test_switch_uses_declared_dependency_branch_not_core_branch(self):
        self.assertEqual(self.run_switch(), 0)
        self.assertEqual(self.mutations(), [
            ("core", ("switch", "--no-overwrite-ignore", "--no-guess", "conference")),
            ("dep", ("switch", "--no-overwrite-ignore", "--no-guess", "dependency-release")),
        ])

    def test_remote_only_core_reads_remote_sources_and_creates_tracking_branch(self):
        self.missing.add(("core", "refs/heads/conference"))
        self.assertEqual(self.run_switch(), 0)
        self.assertIn(("core", ("show", "refs/remotes/origin/conference:pyproject.toml")), self.calls)
        self.assertEqual(self.mutations()[0][1],
                         ("switch", "--no-overwrite-ignore", "--track", "-c", "conference", "origin/conference"))

    def test_dirty_dependency_blocks_before_core_switch(self):
        self.dirty = "dep"
        with self.assertRaisesRegex(ValueError, "uncommitted"):
            self.run_switch()
        self.assertFalse(self.mutations())

    def test_dirty_core_blocks_before_reading_committed_sources(self):
        self.dirty = "core"
        with self.assertRaisesRegex(ValueError, "uncommitted"):
            self.run_switch()
        self.assertFalse(any(args[0] == "show" for _, args in self.calls))
        self.assertFalse(self.mutations())

    def test_missing_dependency_branch_blocks_before_core_switch(self):
        self.missing.update({("dep", "refs/heads/dependency-release"),
                             ("dep", "refs/remotes/origin/dependency-release")})
        with self.assertRaisesRegex(ValueError, "missing ref"):
            self.run_switch()
        self.assertFalse(self.mutations())

    def test_occupied_branch_blocks_before_core_switch(self):
        self.occupied = True
        with self.assertRaisesRegex(ValueError, "another worktree"):
            self.run_switch()
        self.assertFalse(self.mutations())

    def test_partial_failure_returns_nonzero_without_rollback(self):
        self.fail_switch = "dep"
        self.assertEqual(self.run_switch(), 1)
        self.assertEqual([name for name, _ in self.mutations()], ["core", "dep"])

    def test_revision_source_blocks_before_mutation(self):
        self.sources = self.sources.replace('branch = "dependency-release"', 'rev = "abcdef"')
        with self.assertRaisesRegex(ValueError, "revision/tag"):
            self.run_switch()
        self.assertFalse(self.mutations())

    def test_active_operation_blocks_before_mutation(self):
        marker = self.root / "dep/.git/MERGE_HEAD"
        marker.parent.mkdir(parents=True)
        marker.write_text("in progress")
        with self.assertRaisesRegex(ValueError, "operation in progress"):
            self.run_switch()
        self.assertFalse(self.mutations())

    def test_setup_override_only_changes_clone_target(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(self.workspace.setup(True, "conference"), 0)
        self.assertIn("PLAN core: conference", output.getvalue())
        self.assertEqual(self.workspace.core["branch"], "old")
        self.assertFalse(self.mutations())

    def test_status_treats_core_manifest_branch_as_clone_default(self):
        for repo in self.workspace.repos:
            self.workspace.path(repo).mkdir()
        with patch.object(self.workspace, "target", return_value={"git": "unused", "branch": "conference"}):
            rows = self.workspace.status()
        self.assertEqual(rows[0]["expected"], "old")
        self.assertNotIn("branch mismatch", rows[0]["issues"])
        self.assertIn("branch mismatch", rows[1]["issues"])

    def test_editable_sources_use_selected_core_clone_metadata(self):
        self.sources = '''[tool.uv.sources]
dep = {path = "../dep", editable = true}
utility = {path = "../utility", editable = true}
[tool.freemocap.workspace.sources]
dep = {git = "https://example.com/dep", branch = "local-release"}
utility = {git = "https://example.com/utility"}
'''
        self.assertEqual(self.run_switch(True), 0)
        self.assertIn(("dep", ("check-ref-format", "--branch", "local-release")), self.calls)
        self.assertFalse(self.mutations())

    def test_editable_path_must_match_manifest(self):
        self.sources = '''[tool.uv.sources]
dep = {path = "../wrong-checkout", editable = true}
'''
        with self.assertRaisesRegex(ValueError, "manifest checkout"):
            self.run_switch()
        self.assertFalse(self.mutations())

    def test_editable_source_requires_clone_metadata(self):
        self.sources = '''[tool.uv.sources]
dep = {path = "../dep", editable = true}
'''
        with self.assertRaisesRegex(ValueError, "clone metadata"):
            self.run_switch()
        self.assertFalse(self.mutations())


if __name__ == "__main__":
    unittest.main()
