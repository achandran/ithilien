import sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from install import Installer
class FirefoxInstall(unittest.TestCase):
    def test_developer_profile_preserved_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp, patch('install.sys.platform','darwin'):
            home=Path(tmp);base=home/'Library/Application Support/Firefox';dev=base/'Profiles/dev';other=base/'Profiles/release'
            (dev/'chrome').mkdir(parents=True);other.mkdir(parents=True)
            (base/'profiles.ini').write_text('[Profile0]\nName=dev-edition-default\nIsRelative=1\nPath=Profiles/dev\n[Profile1]\nName=default\nIsRelative=1\nPath=Profiles/release\n')
            css=dev/'chrome/userContent.css';css.write_text('body { color: navy; }\n')
            js=dev/'user.js';js.write_text('user_pref("example", 1);\n')
            Installer(home).firefox();self.assertEqual(css.read_text(),'body { color: navy; }\n')
            i=Installer(home,True);i.firefox();first=css.read_bytes();i.firefox()
            self.assertEqual(first,css.read_bytes());self.assertIn('body { color: navy; }',css.read_text());self.assertIn('#8B3037',css.read_text())
            self.assertIn('user_pref("example", 1);',js.read_text());self.assertIn('stylesheets", true',js.read_text())
            self.assertFalse((other/'user.js').exists());self.assertTrue(i.backup.exists())
