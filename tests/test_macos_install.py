import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install import Installer

class MacOSInstall(unittest.TestCase):
    def test_dry_run_apply_and_backup(self):
        with tempfile.TemporaryDirectory() as tmp, patch('install.sys.platform', 'darwin'), patch('install.subprocess.run') as run:
            run.return_value = subprocess.CompletedProcess([], 0, 'old value\n', '')
            installer = Installer(Path(tmp))
            installer.macos()
            self.assertEqual(run.call_count, 1)
            self.assertFalse(installer.backup.exists())
            installer.apply = True
            installer.macos()
            self.assertEqual(run.call_args.args[0], ['/usr/bin/defaults', 'write', '-g', 'AppleHighlightColor', '-string', '0.658824 0.698039 0.682353 Other'])
            self.assertEqual(json.loads((installer.backup / 'macos-highlight.json').read_text())['previous'], 'old value')

    def test_unchanged_and_non_mac(self):
        with tempfile.TemporaryDirectory() as tmp, patch('install.subprocess.run') as run:
            installer = Installer(Path(tmp), True)
            with patch('install.sys.platform', 'linux'):
                installer.macos()
                run.assert_not_called()
                self.assertFalse(installer.detected('macos', 'macOS'))
            with patch('install.sys.platform', 'darwin'):
                run.return_value = subprocess.CompletedProcess([], 0, '0.658824 0.698039 0.682353 Other\n', '')
                installer.macos()
                self.assertEqual(run.call_count, 1)
                self.assertFalse(installer.backup.exists())
