import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install import Installer, managed_config


class InstallTests(unittest.TestCase):
    def test_config_idempotent_preserves_other_settings(self):
        original = '# personal\nfont-size = 15\ntheme = old\n'
        result = managed_config(original, 'new')
        self.assertIn('font-size = 15', result)
        self.assertNotIn('theme = old', result)
        self.assertEqual(result, managed_config(result, 'new'))

    def test_malformed_block_rejected(self):
        with self.assertRaises(ValueError):
            managed_config('# BEGIN ITHILIEN\nfont-size = 15', 'new')

    def test_dry_run_backup_and_idempotence(self):
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            home = Path(temp); target = home / 'config'; target.write_text('original')
            dry = Installer(home); dry.write(target, b'new')
            self.assertEqual(target.read_text(), 'original')
            self.assertFalse(dry.backup.exists())
            install = Installer(home, True); install.write(target, b'new')
            backups = list(install.backup.rglob('config'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), 'original')
            install.write(target, b'new')
            self.assertEqual(install.count, 1)

    def test_absent_apps_write_nothing(self):
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()), patch.object(Installer, 'detected', return_value=False):
            home = Path(temp)
            self.assertFalse(Installer(home, True).run())
            self.assertEqual(list(home.iterdir()), [])

    def test_symlink_not_replaced(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp); target=home/'real'; target.write_text('keep')
            link=home/'link'; link.symlink_to(target)
            with self.assertRaises(ValueError):
                Installer(home, True).write(link,b'new')
            self.assertEqual(target.read_text(),'keep')
