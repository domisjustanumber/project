"""The agents and ADR kit: its decision log, its module template and its tools (skellytracker ADR-P3NK)."""
import importlib.util
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

KIT_ROOT = Path(__file__).resolve().parents[1] / "agents-and-adr-process" / "bootstrap"
MODULE_ROOT = KIT_ROOT.parent / "module"


def load(path, name):
    """Import a kit tool from its file, under a name of its own."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class KitTests(unittest.TestCase):
    def test_kit_decision_log_passes_the_kit_check(self):
        cdl = load(KIT_ROOT / "tools" / "check_decision_log.py", "kit_check_decision_log")
        self.assertEqual(cdl.check(KIT_ROOT), [])

    def test_kit_with_two_module_logs_passes_the_kit_checks(self):
        """A repo made from the kit with the filled-in module template in server/ and ui/ passes."""
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(KIT_ROOT, root, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
            for module in ("server", "ui"):
                shutil.copytree(MODULE_ROOT, root / module)
                # Fill in as guide step 2 says: each `...{{ROOT}}...` code span becomes a link, with {{ROOT}} = ../.
                for md in (root / module).rglob("*.md"):
                    text = re.sub(r"`([^`]*)\{\{ROOT\}\}([^`]*)`", r"[`\1../\2`](\1../\2)", md.read_text(encoding="utf-8"))
                    self.assertNotIn("{{ROOT}}", text)
                    md.write_text(text.replace("{{MODULE}}", module), encoding="utf-8")
            cdl = load(root / "tools" / "check_decision_log.py", "kit_check_decision_log_modules")
            links = load(root / "tools" / "check_links.py", "kit_check_links_modules")
            logs = (cdl.LOG_DIR, Path("server/decisions"), Path("ui/decisions"))
            with patch.object(cdl, "LOG_DIRS", logs):
                self.assertEqual(cdl.present_logs(root), list(logs))
                self.assertEqual(cdl.check(root), [])
            files = links.markdown_files(root)
            self.assertIn(root / "server" / "decisions" / "README.md", files)
            self.assertEqual([e for f in files for e in links.check_file(f, root)], [])

    def test_kit_tools_have_no_placeholders(self):
        tools = sorted((KIT_ROOT / "tools").rglob("*.py"))
        self.assertTrue(tools)
        for path in tools:
            self.assertNotIn("{{", path.read_text(encoding="utf-8"), path)


if __name__ == "__main__":
    unittest.main()
