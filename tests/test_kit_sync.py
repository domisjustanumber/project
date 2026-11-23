"""The two-way kit sync: pull, propose and the kit manifest (tools/kit_sync.py of the kit).

Each test makes a kit checkout from this working tree in a temporary git repository, and a repository
made from the kit as step 2 and step 3 of agents-and-adr-process/README.md say.
"""
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
KIT = PROJECT / "agents-and-adr-process"
BOOTSTRAP = KIT / "bootstrap"
# The kit tools import tools/kit_config.py. Each tool gives it its own root, so one copy serves all.
sys.path.insert(0, str(BOOTSTRAP / "tools"))
VALUES = {
    "DEFAULT_BRANCH_TEXT": "upstream `development`",
    "AREAS": "the code, the CI",
    "NORMATIVE_DOCS": "the specs in `specs/`",
    "SIBLING_PATH": "../skellyfileformat/spec/",
    "SECRET_SCAN_BRANCHES": "[main, development]",
    "PYTHON_VERSION": "3.13.18",
    "SELF_TEST": "example.certify",
    "CERTIFY_SPEC": "docs/certify-checks.md",
    "CERTIFY_REPO": "example-certify",
    "RULES_ENTRY_LINK": "[ADR-0030](decisions/entries/0030-private-data.md)",
}
# Repositories that use the kit but are not in repos.toml.
OTHER_REPOS = ("skellycertify", "skellyfileformat", "skellyspecs", "OpenMMLab-Exporter")


def load(path, name):
    """Import a kit tool from its file, under a name of its own."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ks = load(BOOTSTRAP / "tools" / "kit_sync.py", "kit_sync_under_test")


def git(cwd, *args):
    subprocess.run(
        ["git", "-c", "user.name=Tester", "-c", "user.email=tester@example.invalid", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
    )


def placeholder(name):
    return "{" * 2 + name + "}" * 2


def fill_known(text):
    """Step 3 of the guide by hand: fill each placeholder that has a value. Keep the others."""
    for name, value in VALUES.items():
        text = text.replace(placeholder(name), value)
    return text


class KitSyncTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        tmp = Path(folder.name)
        environment = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
        environment.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_CEILING_DIRECTORIES=str(tmp))
        patcher = patch.dict(os.environ, environment, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.kit = tmp / "project"
        shutil.copytree(KIT, self.kit / ks.KIT_FOLDER, ignore=shutil.ignore_patterns("__pycache__"))
        git(self.kit, "init", "-q", "-b", "main")
        git(self.kit, "config", "core.autocrlf", "false")
        self.commit_kit("kit")
        self.repo = tmp / "repo"
        self.make_repo()

    # Helpers.

    def commit_kit(self, message):
        git(self.kit, "add", "-A")
        git(self.kit, "commit", "-q", "-m", message)

    def kit_file(self, path):
        return self.kit / ks.KIT_FOLDER / path

    def make_repo(self, fill_by_hand=False):
        """Step 2 (copy) and step 3 (kit.toml, then the first pull) of the guide."""
        if self.repo.exists():
            shutil.rmtree(self.repo)
        shutil.copytree(self.kit_file("bootstrap"), self.repo, ignore=shutil.ignore_patterns("__pycache__"))
        additions = self.repo / "gitignore-additions.txt"
        (self.repo / ".gitignore").write_text("node_modules/\n" + additions.read_text(encoding="utf-8"), encoding="utf-8")
        additions.unlink()
        for path in self.repo.rglob("*") if fill_by_hand else ():
            if path.is_file() and path.name != "kit.toml":
                path.write_text(fill_known(path.read_text(encoding="utf-8")), encoding="utf-8", newline="")
        config = (self.repo / "kit.toml").read_text(encoding="utf-8")
        for name, value in VALUES.items():
            config = re.sub(rf'^{name} = "[^"]*"', f'{name} = "{value}"', config, flags=re.MULTILINE)
        (self.repo / "kit.toml").write_text(config, encoding="utf-8", newline="\n")
        self.pull()

    def pull(self, *replace):
        return ks.pull(self.repo, self.kit, "HEAD", frozenset(replace))

    def propose(self, *ids, new=(), fill=(), literal=()):
        return ks.propose(self.repo, self.kit, list(ids) or None, list(new), frozenset(fill), frozenset(literal))

    def snapshot(self):
        return {p.relative_to(self.repo).as_posix(): p.read_bytes() for p in sorted(self.repo.rglob("*")) if p.is_file()}

    def edit(self, path, old, new):
        target = path if isinstance(path, Path) else self.repo / path
        text = target.read_text(encoding="utf-8")
        self.assertEqual(text.count(old), 1, old)
        target.write_text(text.replace(old, new), encoding="utf-8", newline="")

    def append(self, path, text):
        with path.open("a", encoding="utf-8", newline="") as file:
            file.write(text)

    def check_errors(self):
        return ks.check(self.repo)[0]

    # Tests.

    def test_a_new_repository_takes_the_kit_and_a_second_pull_changes_nothing(self):
        state = ks.load_config(self.repo)["kit"]
        units = ks.chosen(ks.parse_manifest(self.kit_file("manifest.toml").read_text(encoding="utf-8"), "m"), {})
        self.assertEqual(sorted(state["hashes"]), sorted(u.id for u in units))
        self.assertEqual(self.check_errors(), [])
        before = self.snapshot()
        self.pull()
        self.assertEqual(self.snapshot(), before)
        workflow = (self.repo / ".github/workflows/secrets.yml").read_text(encoding="utf-8")
        self.assertIn(f"branches: {VALUES['SECRET_SCAN_BRANCHES']}", workflow)
        skill = (self.repo / ".claude/skills/change-decision-log/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(f"Until a commit is on {VALUES['DEFAULT_BRANCH_TEXT']}, cite", skill)

    def test_pull_writes_lf_line_ends(self):
        """Each repository uses LF line ends on each system. A CRLF working file that pull writes gets LF."""
        agents = self.repo / "AGENTS.md"
        agents.write_bytes(agents.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.edit(self.kit_file("bootstrap/AGENTS.md"), "Use short sentences.", "Use short sentences. Use short words.")
        self.commit_kit("change")
        self.pull()
        data = agents.read_bytes()
        self.assertIn(b"Use short words.", data)
        self.assertNotIn(b"\r\n", data)
        self.assertEqual(self.check_errors(), [])

    def test_a_copy_filled_in_by_hand_takes_the_kit_with_no_change(self):
        self.make_repo(fill_by_hand=True)
        before = self.snapshot()
        self.pull()
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.check_errors(), [])

    def test_pull_takes_a_kit_change_when_the_local_text_did_not_change(self):
        self.edit(self.kit_file("bootstrap/AGENTS.md"), "Use short sentences.", "Use short sentences. Use short words.")
        self.append(self.kit_file("bootstrap/tools/check_links.py"), "# A new line.\n")
        self.commit_kit("change")
        self.pull()
        self.assertIn("Use short words.", (self.repo / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn("# A new line.", (self.repo / "tools/check_links.py").read_text(encoding="utf-8"))
        self.assertEqual(self.check_errors(), [])

    def test_a_local_change_fails_check_until_propose_and_the_kit_takes_it(self):
        old = f"before you change {VALUES['AREAS']} or these instructions."
        self.edit("AGENTS.md", old, f"before you change {VALUES['AREAS']}, the docs or these instructions.")
        self.assertEqual([e.split(":")[0] for e in self.check_errors()], ["AGENTS.md#decision-log"])
        notes = self.propose()
        self.assertTrue(any("AGENTS.md#decision-log: wrote" in n for n in notes), notes)
        kit_text = self.kit_file("bootstrap/AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(f"before you change {placeholder('AREAS')}, the docs or these instructions.", kit_text)
        self.assertNotIn(VALUES["AREAS"], kit_text)
        self.assertEqual(self.check_errors(), [], "a proposed change waits for the kit")
        # A pull before the kit takes the change keeps the local change.
        notes = self.pull()
        self.assertTrue(any("kept the local change" in n for n in notes), notes)
        self.assertEqual(self.check_errors(), [])
        self.commit_kit("take the change")
        before = (self.repo / "AGENTS.md").read_bytes()
        self.pull()
        self.assertEqual((self.repo / "AGENTS.md").read_bytes(), before)
        self.assertNotIn("pending", ks.load_config(self.repo)["kit"])
        self.assertEqual(self.check_errors(), [])

    def test_propose_refuses_a_value_that_has_no_placeholder_in_the_kit_text(self):
        self.edit(
            "AGENTS.md",
            "Write the summary in the message text, not only in the tool description.\n",
            "Write the summary in the message text, not only in the tool description.\n"
            f"Name the branch {VALUES['DEFAULT_BRANCH_TEXT']} when the call pushes.\n",
        )
        before = self.kit_file("bootstrap/AGENTS.md").read_bytes()
        with self.assertRaisesRegex(ks.KitError, "give --fill NAME or --literal NAME"):
            self.propose()
        self.assertEqual(self.kit_file("bootstrap/AGENTS.md").read_bytes(), before)
        self.propose(fill=["DEFAULT_BRANCH_TEXT"])
        kit_text = self.kit_file("bootstrap/AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(f"Name the branch {placeholder('DEFAULT_BRANCH_TEXT')} when the call pushes.", kit_text)

    def test_propose_keeps_a_placeholder_in_a_paragraph_that_is_wrapped_again(self):
        old = (
            f"[`open-work.md`](decisions/open-work.md) before you change {VALUES['AREAS']} or these instructions.\n"
            "For a task in a module with a log, also read the `decisions/README.md` and the\n"
        )
        new = (
            f"[`open-work.md`](decisions/open-work.md) first, before you change {VALUES['AREAS']} or these\n"
            "instructions. For a task in a module with a log, also read the `decisions/README.md` and the\n"
        )
        self.edit("AGENTS.md", old, new)
        self.propose()
        kit_text = self.kit_file("bootstrap/AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(f"first, before you change {placeholder('AREAS')} or these\ninstructions.", kit_text)

    def test_propose_refuses_a_citation_of_an_entry_of_the_repository(self):
        self.edit(
            "AGENTS.md",
            "Write the summary in the message text, not only in the tool description.\n",
            "Write the summary in the message text, not only in the tool description (ADR-VV4Q).\n",
        )
        with self.assertRaisesRegex(ks.KitError, "cites only the kit entry 0001; remove or replace ADR-VV4Q"):
            self.propose()

    def test_pull_refuses_when_the_kit_and_the_local_text_both_changed(self):
        self.edit(self.kit_file("bootstrap/AGENTS.md"), "Use short sentences.", "Use short sentences. Kit change.")
        self.commit_kit("kit change")
        self.edit("AGENTS.md", "Use short sentences.", "Use short sentences. Local change.")
        before = self.snapshot()
        with self.assertRaisesRegex(ks.KitError, "both changed"):
            self.pull()
        self.assertEqual(self.snapshot(), before)
        self.pull("AGENTS.md#writing-rules")
        self.assertIn("Kit change.", (self.repo / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertEqual(self.check_errors(), [])

    def test_propose_refuses_when_the_kit_head_changed_the_unit(self):
        self.edit(self.kit_file("bootstrap/AGENTS.md"), "Use short sentences.", "Use short sentences. Kit change.")
        self.commit_kit("kit change")
        self.edit("AGENTS.md", "Use short sentences.", "Use short sentences. Local change.")
        with self.assertRaisesRegex(ks.KitError, "run pull first"):
            self.propose()

    def test_pull_refuses_a_differing_unit_with_no_hash_unless_replace(self):
        self.append(self.kit_file("bootstrap/tools/check_links.py"), "# A new line.\n")
        self.edit(self.kit_file("manifest.toml"), 'path = "tools/check_links.py"\n', 'path = "tools/check_links.py"\n\n[[file]]\npath = "tools/extra.py"\n')
        (self.kit_file("bootstrap/tools/extra.py")).write_text("kit = 1\n", encoding="utf-8")
        self.commit_kit("new unit")
        (self.repo / "tools/extra.py").write_text("mine = 1\n", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaisesRegex(ks.KitError, "--replace tools/extra.py"):
            self.pull()
        self.assertEqual(self.snapshot(), before, "a refusal writes nothing")
        self.pull("tools/extra.py")
        self.assertEqual((self.repo / "tools/extra.py").read_text(encoding="utf-8"), "kit = 1\n")
        self.assertIn("# A new line.", (self.repo / "tools/check_links.py").read_text(encoding="utf-8"))

    def test_propose_adds_a_new_block_and_a_new_file(self):
        self.edit(
            "AGENTS.md",
            "Do not change code that your task does not need.\n",
            "Do not change code that your task does not need.\n\n<!-- kit:example-rule -->\nTest only here.\n<!-- /kit -->\n",
        )
        (self.repo / "tools/check_new.py").write_text("print('new')\n", encoding="utf-8")
        with self.assertRaisesRegex(ks.KitError, "add its two marker lines first"):
            self.propose(new=["AGENTS.md#example-rule"])
        self.edit(
            self.kit_file("bootstrap/AGENTS.md"),
            "Do not change code that your task does not need.\n",
            "Do not change code that your task does not need.\n\n<!-- kit:example-rule -->\n<!-- /kit -->\n",
        )
        self.propose(new=["AGENTS.md#example-rule", "tools/check_new.py"])
        manifest = ks.parse_manifest(self.kit_file("manifest.toml").read_text(encoding="utf-8"), "m")
        self.assertIn("AGENTS.md#example-rule", [u.id for u in manifest])
        self.assertIn("tools/check_new.py", [u.id for u in manifest])
        self.assertIn("<!-- kit:example-rule -->\nTest only here.\n<!-- /kit -->", self.kit_file("bootstrap/AGENTS.md").read_text(encoding="utf-8"))
        self.assertEqual(self.kit_file("bootstrap/tools/check_new.py").read_text(encoding="utf-8"), "print('new')\n")
        self.commit_kit("new units")
        self.pull()
        self.assertIn("AGENTS.md#example-rule", ks.load_config(self.repo)["kit"]["hashes"])
        self.assertEqual(self.check_errors(), [])

    def test_a_pull_that_changes_kit_sync_runs_the_new_tool_once_more(self):
        self.append(self.kit_file("bootstrap/tools/kit_sync.py"), "# A new version of the tool.\n")
        self.commit_kit("new tool")
        run = subprocess.run(
            [sys.executable, str(self.repo / "tools" / "kit_sync.py"), "pull", "--kit", str(self.kit)],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(run.stdout.count("the new tool runs the pull once more"), 1, run.stdout)
        self.assertIn("# A new version of the tool.", (self.repo / "tools" / "kit_sync.py").read_text(encoding="utf-8"))
        self.assertEqual(self.check_errors(), [])

    def test_check_finds_a_value_that_pull_did_not_fill_in(self):
        self.edit("kit.toml", f'AREAS = "{VALUES["AREAS"]}"', 'AREAS = "the code"')
        self.assertEqual([e.split(":")[0] for e in self.check_errors()], ["kit"])
        self.pull()
        self.assertIn("before you change the code or these instructions.", (self.repo / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertEqual(self.check_errors(), [])

    def test_the_advice_of_check_names_replace_and_propose(self):
        self.edit("AGENTS.md", "Use short sentences.", "Use short sentences. Local change.")
        self.pull()
        [error] = self.check_errors()
        self.assertIn("pull --replace AGENTS.md#writing-rules", error)
        self.assertIn("propose", error)

    def test_a_unit_that_the_repository_skips_is_not_written(self):
        self.edit("kit.toml", "# skip = [", 'skip = [".github/workflows/doc-checks.yml"]\n# skip = [')
        self.pull()
        self.assertNotIn(".github/workflows/doc-checks.yml", ks.load_config(self.repo)["kit"]["hashes"])
        self.assertEqual(self.check_errors(), [])


class KitManifestTests(unittest.TestCase):
    def setUp(self):
        self.units = ks.parse_manifest((KIT / "manifest.toml").read_text(encoding="utf-8"), "manifest.toml")
        self.texts = {}
        for unit in self.units:
            text = ks.unit_text(ks.read_file(KIT / unit.kit), unit, unit.kit)
            self.assertIsNotNone(text, f"{unit.id}: no kit text in {unit.kit}")
            self.texts[unit.id] = text

    def test_each_placeholder_of_a_unit_has_a_value_in_the_kit_toml_template(self):
        with (BOOTSTRAP / "kit.toml").open("rb") as file:
            values = ks.check_values(tomllib.load(file)["values"])
        for uid, text in self.texts.items():
            self.assertNotRegex(text, r"\{\{[A-Z_]+[,:]", f"{uid}: a placeholder in a unit has no hint text")
            ks.fill(text, values, uid)

    def test_no_repository_value_in_a_kit_unit(self):
        with (PROJECT / "repos.toml").open("rb") as file:
            names = [r["name"] for r in tomllib.load(file)["repos"]] + list(OTHER_REPOS)
        pattern = re.compile(r"(?<![\w-])(?:" + "|".join(map(re.escape, names)) + r")(?![\w-])", re.IGNORECASE)
        for uid, text in self.texts.items():
            found = sorted({m.group() for m in pattern.finditer(text.replace("freemocap/project", ""))})
            self.assertEqual(found, [], uid)
            for name, value in VALUES.items():
                if len(value) > 8:
                    self.assertNotIn(value, text, f"{uid}: the value of {name} of a test repository")

    def test_no_unit_cites_an_entry_other_than_0001(self):
        for unit in self.units:
            self.assertEqual(ks.entry_citations(self.texts[unit.id], unit.path), [], unit.id)

    def test_gitleaks_allows_the_hashes_of_kit_toml(self):
        config = tomllib.loads(self.texts[".gitleaks.toml#gitleaks-config"])
        rows = [a for a in config["allowlists"] if a.get("paths") == ["^kit\\.toml$"]]
        self.assertEqual(len(rows), 1)
        self.assertRegex("0" * 64, rows[0]["regexes"][0])

    def test_a_path_value_in_a_link_target_becomes_its_placeholder(self):
        unfill = ks.Unfill({"SPEC": "specs/certify.md"})
        kit = "Read [the spec](../../../" + placeholder("SPEC") + ")."
        local = "Read [the spec](../../../specs/certify.md) first."
        self.assertEqual(unfill.text(kit, local, "u")[0], "Read [the spec](../../../" + placeholder("SPEC") + ") first.")
        with self.assertRaises(ks.KitError):
            unfill.text("", "See ../specs/certify.md.", "u")

    def test_a_name_value_in_a_url_is_found(self):
        unfill = ks.Unfill({"REPO": "skellycertify"})
        kit = "See https://github.com/o/" + placeholder("REPO") + "/blob/main/x.md."
        local = "See https://github.com/o/skellycertify/blob/main/x.md first."
        self.assertEqual(unfill.text(kit, local, "u")[0], "See https://github.com/o/" + placeholder("REPO") + "/blob/main/x.md first.")
        with self.assertRaisesRegex(ks.KitError, "REPO"):
            unfill.text("", "A new line: https://github.com/o/skellycertify/blob/main/y.md", "u")

    def test_each_marker_block_of_a_kit_file_is_in_the_manifest(self):
        listed = {u.id for u in self.units}
        for kit_path in sorted({u.kit for u in self.units if u.block}):
            path = next(u.path for u in self.units if u.kit == kit_path)
            for name in ks.blocks((KIT / kit_path).read_text(encoding="utf-8"), kit_path):
                self.assertIn(f"{path}#{name}", listed)

    def test_the_tools_read_their_values_from_kit_toml(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(BOOTSTRAP / "tools", root / "tools", ignore=shutil.ignore_patterns("__pycache__"))
            (root / "kit.toml").write_text(
                "[check_decision_log]\nmodule_logs = [\"m/decisions\"]\ntarget_branch = \"development\"\n"
                "index_limit = 24_000\n\n[check_private_data]\nallowed_emails = [\"Contact@Example.org\"]\n"
                "[[check_private_data.allowed_lines]]\npath = \"a.md\"\nline = 3\nsha256 = \"" + "0" * 64 + "\"\nreason = \"r\"\n\n"
                "[check_camera_media]\ngolden_paths = [\"media/\"]\n",
                encoding="utf-8",
            )
            cdl = load(root / "tools" / "check_decision_log.py", "kit_cdl_values")
            cpd = load(root / "tools" / "check_private_data.py", "kit_cpd_values")
            ccm = load(root / "tools" / "check_camera_media.py", "kit_ccm_values")
            self.assertEqual(cdl.LOG_DIRS, (Path("decisions"), Path("m/decisions")))
            self.assertEqual((cdl.TARGET_BRANCH, cdl.INDEX_LIMIT, cdl.READ_PATH_LIMIT), ("development", 24_000, 220_000))
            self.assertIn("contact@example.org", cpd.ALLOWED_EMAILS)
            self.assertEqual(cpd.ALLOWED_LINES, {("a.md", 3): ("0" * 64, "r")})
            self.assertEqual(ccm.GOLDEN_PATHS, ("media/",))
            # Fail closed: a misspelt key, a misspelt or missing table, or a value of the wrong type stops the tool.
            for config in (
                "[check_camera_media]\ngolden_path = []\n",
                "[check_camera_medai]\ngolden_paths = []\n",
                "[check_decision_log]\n",
            ):
                (root / "kit.toml").write_text(config, encoding="utf-8")
                with self.assertRaises(SystemExit, msg=config):
                    load(root / "tools" / "check_camera_media.py", "kit_ccm_closed")
            for config in ('[check_decision_log]\nmodule_logs = "m/decisions"\n', '[check_decision_log]\nindex_limit = "24000"\n'):
                (root / "kit.toml").write_text(config, encoding="utf-8")
                with self.assertRaisesRegex(SystemExit, "the value must be", msg=config):
                    load(root / "tools" / "check_decision_log.py", "kit_cdl_types")
            # With an empty table, the default of golden_paths allows no golden file.
            (root / "kit.toml").write_text("[check_camera_media]\n", encoding="utf-8")
            self.assertEqual(load(root / "tools" / "check_camera_media.py", "kit_ccm_default").GOLDEN_PATHS, ())


if __name__ == "__main__":
    unittest.main()
