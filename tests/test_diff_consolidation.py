"""Keep one line color per diff state and shared amber for edited spans."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ithilienlib import ROOT, load_palette, wcag

class FourColorDiff(unittest.TestCase):
    def test_line_and_inline_background_contract(self):
        d=load_palette('ithilien-dawn')['diff']
        lines=[d[k+'Background'] for k in ('add','delete','change')]
        self.assertEqual(len(set(lines)),3)
        self.assertNotIn(d['changeEmphasis'],lines)
        for kind in ('add','delete','change'):
            self.assertEqual(d[kind+'Emphasis'],d['changeEmphasis'])
            self.assertGreaterEqual(wcag(d['inlineForeground'],d[kind+'Emphasis']),7)

    def test_shipped_claude_word_roles_preserve_line_direction(self):
        c=json.loads((ROOT/'extras/claude-code/themes/ithilien-dawn.json').read_text())['overrides']
        d=load_palette('ithilien-dawn')['diff']
        self.assertEqual(c['diffAddedWord'],d['changeEmphasis'])
        self.assertEqual(c['diffRemovedWord'],d['changeEmphasis'])
        self.assertNotEqual(c['diffAdded'],c['diffRemoved'])
