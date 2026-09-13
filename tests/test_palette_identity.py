"""Freeze the selected Formex Dawn and Warm Graphite Dusk."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ithilienlib import load_palette

# Names may evolve; canonical colors, polarity and semantic assignments are frozen.
# Updating these fingerprints must accompany an explicitly intended palette change.
EXPECTED = {'dusk': 'f7ae343f6908f591c4517842ce8df1b62e303ecade9b581ce33f03d634ccd60d', 'dawn': 'd8ceb1384c12525bbdcee723555e174b5898cc311b05aab3c7f44587cda39e35'}

class PaletteIdentity(unittest.TestCase):
    def test_selected_palettes(self):
        for variant, expected in EXPECTED.items():
            with self.subTest(variant=variant):
                palette = load_palette('ithilien-' + variant)
                palette = {k: v for k, v in palette.items() if k not in {'name', 'slug'}}
                actual = hashlib.sha256(json.dumps(palette, sort_keys=True).encode()).hexdigest()
                self.assertEqual(actual, expected, 'Palette changed from approved Dawn / Warm Graphite Dusk baseline')
