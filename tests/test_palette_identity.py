"""Freeze the selected Reef Green Dawn and Dusk."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ithilienlib import load_palette

# Names may evolve; canonical colors, polarity and semantic assignments are frozen.
# Updating these fingerprints must accompany an explicitly intended palette change.
EXPECTED = {'dusk': 'a82c0cc679db135f048d8f6bee44499323633fa9f693f3988e4d83ba472e0572', 'dawn': '20f71e7244ca833c59949d9ac150303ff1761cd46235c0e6dff14d8b8256d5d3'}

class PaletteIdentity(unittest.TestCase):
    def test_selected_palettes(self):
        for variant, expected in EXPECTED.items():
            with self.subTest(variant=variant):
                palette = load_palette('ithilien-' + variant)
                palette = {k: v for k, v in palette.items() if k not in {'name', 'slug'}}
                actual = hashlib.sha256(json.dumps(palette, sort_keys=True).encode()).hexdigest()
                self.assertEqual(actual, expected, 'Palette changed from approved Reef Green Dawn / Dusk baseline')
