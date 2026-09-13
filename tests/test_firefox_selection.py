import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ithilienlib import ROOT, load_palette, wcag

class FirefoxSelectionTests(unittest.TestCase):
    def test_variant_selection_and_scheme_match_palette(self):
        for variant in ('dawn',):
            p=load_palette('ithilien-'+variant)
            base=ROOT/'extras/firefox'/('ithilien-'+variant)
            theme=json.loads((base/'manifest.json').read_text())['theme']
            c=theme['colors']
            self.assertEqual(theme['properties']['color_scheme'],p['polarity'])
            self.assertEqual(c['toolbar_field_highlight'],p['highlight']['background'])
            self.assertEqual(c['toolbar_field_highlight_text'],p['highlight']['foreground'])
            self.assertGreaterEqual(wcag(c['toolbar_field_highlight_text'],c['toolbar_field_highlight']),4.5)
            self.assertIn(p['highlight']['background'],(base/'userContent.css').read_text())
