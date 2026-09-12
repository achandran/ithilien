import os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from install import Installer
class NeovimInstall(unittest.TestCase):
    def test_existing_spec_migrates_only_unmodified_generated_file(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ,{},clear=True):
            home=Path(tmp);plugins=home/'.config/nvim/lua/plugins';plugins.mkdir(parents=True)
            user=plugins/'colorscheme.lua';user.write_text('return {{"LazyVim/LazyVim"}}')
            Installer(home,True).nvim()
            managed=plugins/'ithilien-installed.lua';self.assertTrue(managed.exists())
            original='return {{"LazyVim/LazyVim"}, {"achandran/ithilien", branch="main"}}'
            user.write_text(original)
            Installer(home).nvim();self.assertTrue(managed.exists())
            installer=Installer(home,True);installer.nvim()
            self.assertFalse(managed.exists());self.assertEqual(user.read_text(),original)
            self.assertTrue(list(installer.backup.rglob('ithilien-installed.lua')))
            Installer(home,True).nvim();self.assertFalse(managed.exists())
            managed.write_text('-- custom\nreturn {}')
            Installer(home,True).nvim();self.assertTrue(managed.exists())
