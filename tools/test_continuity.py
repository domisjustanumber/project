"""Verify global installation preserves user content and fails without partial edits."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'scripts/install_continuity_guidance.py'
SPEC = importlib.util.spec_from_file_location('continuity_installer', SOURCE)
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


class InstallationTests(unittest.TestCase):
    def test_install_preserves_existing_guidance_and_is_idempotent(self):
        with tempfile.TemporaryDirectory(prefix='continuity-install-') as directory:
            home = Path(directory)
            (home / 'AGENTS.md').write_text('Personal instructions.\n', encoding='utf-8')
            checklist = home / 'skills/linear-checklist-task/SKILL.md'
            checklist.parent.mkdir(parents=True)
            checklist.write_text('Existing approval and ordering rules.\n', encoding='utf-8')
            (home / 'config.toml').write_text('model = "unchanged"\n', encoding='utf-8')
            self.assertEqual(len(INSTALLER.install(home)), 3)
            self.assertTrue((home / 'AGENTS.md').read_text().startswith('Personal instructions.\n'))
            self.assertTrue(checklist.read_text().startswith('Existing approval and ordering rules.\n'))
            self.assertEqual(INSTALLER.install(home), [])
            self.assertEqual((home / 'config.toml').read_text(), 'model = "unchanged"\n')

    def test_conflicting_skill_preserves_every_existing_file(self):
        with tempfile.TemporaryDirectory(prefix='continuity-conflict-') as directory:
            home = Path(directory)
            target = home / 'skills/context-continuity/SKILL.md'
            target.parent.mkdir(parents=True)
            target.write_text('User-authored skill', encoding='utf-8')
            with self.assertRaises(ValueError):
                INSTALLER.install(home)
            self.assertFalse((home / 'AGENTS.md').exists())
            self.assertEqual(target.read_text(), 'User-authored skill')

    def test_damaged_delimiters_are_rejected(self):
        for content in [INSTALLER.START, INSTALLER.END,
                        INSTALLER.END + INSTALLER.START,
                        (INSTALLER.START + INSTALLER.END) * 2]:
            with self.subTest(content=content), self.assertRaises(ValueError):
                INSTALLER.merge(content, 'replacement')

    def test_update_changes_only_managed_block(self):
        before = 'Owner prefix\n' + INSTALLER.START + '\nold\n' + INSTALLER.END + '\nOwner suffix'
        expected = 'Owner prefix\n' + INSTALLER.START + '\nnew\n' + INSTALLER.END + '\nOwner suffix'
        self.assertEqual(INSTALLER.merge(before, 'new'), expected)


if __name__ == '__main__':
    unittest.main()
