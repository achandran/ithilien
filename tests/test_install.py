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

    def test_ghostty_always_uses_home_config_even_with_native_and_xdg_override(self):
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            home = Path(temp)
            native = home / 'Library/Application Support/com.mitchellh.ghostty/config'
            native.parent.mkdir(parents=True)
            native.write_text('theme = native-theme\n')
            config = home / '.config/ghostty/config'
            config.parent.mkdir(parents=True)
            config.write_text('font-size = 15\ntheme = old\n')
            with patch.dict('os.environ', {'XDG_CONFIG_HOME': str(home / 'alternative')}):
                installer = Installer(home, True)
                installer.ghostty()
                writes = installer.count
                installer.ghostty()
                self.assertEqual(installer.count, writes)
            self.assertEqual(native.read_text(), 'theme = native-theme\n')
            self.assertIn('font-size = 15', config.read_text())
            self.assertIn('theme = light:ithilien_dawn.conf,dark:ithilien_dusk.conf', config.read_text())
            for variant in ('dawn', 'dusk'):
                self.assertTrue((config.parent / 'themes' / f'ithilien_{variant}.conf').is_file())
            self.assertFalse((home / 'alternative').exists())
            self.assertTrue(installer.backup.exists())

    def test_zsh_installs_source_once_and_preserves_other_styles(self):
        import subprocess
        import shutil
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            home=Path(temp); rc=home/'.zshrc'; rc.write_text('bindkey -v\nzle_highlight=("paste:none" "region:bg=#B17232,fg=#000000")\n')
            with patch.dict('os.environ', {'XDG_CONFIG_HOME': str(home/'.config'), 'ZDOTDIR': str(home)}):
                installer=Installer(home,True); installer.zsh(); count=installer.count; installer.zsh()
            self.assertEqual(installer.count,count)
            self.assertEqual(rc.read_text().count('# BEGIN ITHILIEN ZLE'),1)
            self.assertIn('bindkey -v',rc.read_text())
            if shutil.which('zsh'):
                script=rc
                self.assertIn('region:bg=#C4CAC8,fg=#000000', rc.read_text())
                result=subprocess.run(['zsh','-f','-c','zle_highlight=("paste:none" "region:standout"); source "$1"; source "$1"; print -l -- "${zle_highlight[@]}"','test',str(script)],capture_output=True,text=True,check=True)
                self.assertEqual(result.stdout.splitlines(),['paste:none','region:bg=#C4CAC8,fg=#000000'])

    def test_installed_prompt_uses_rosehip_and_keeps_git_variable(self):
        import subprocess
        import shutil
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            home=Path(temp); rc=home/'.zshrc'
            rc.write_text("export PS1='old prompt'\nvcs_info_msg_0_='main'\n")
            with patch.dict('os.environ', {'XDG_CONFIG_HOME': str(home/'.config'), 'ZDOTDIR': str(home)}):
                installer=Installer(home,True);installer.zsh();installer.zsh()
            self.assertEqual(rc.read_text().count('# BEGIN ITHILIEN ZLE'),1)
            if shutil.which('zsh'):
                result=subprocess.run(['zsh','-f','-c','source "$1"; [[ -o promptsubst ]] || exit 1; print -r -- "$PS1"; print -r -- "$vcs_info_msg_0_"','test',str(rc)],capture_output=True,text=True,check=True)
                self.assertIn('%F{9}%m%f',result.stdout)
                self.assertIn('${vcs_info_msg_0_}',result.stdout)
                self.assertIn('\n%f$ ',result.stdout)
                self.assertTrue(result.stdout.endswith('main\n'))
