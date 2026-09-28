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
EXPECTED = {'dusk': 'a82c0cc679db135f048d8f6bee44499323633fa9f693f3988e4d83ba472e0572', 'dawn': '0eafd623d2682fb068899a0c793c8fa02af45f87f72c61a5f4abca2d57eedc9e'}

class PaletteIdentity(unittest.TestCase):
    def test_selected_palettes(self):
        for variant, expected in EXPECTED.items():
            with self.subTest(variant=variant):
                palette = load_palette('ithilien-' + variant)
                palette = {k: v for k, v in palette.items() if k not in {'name', 'slug'}}
                actual = hashlib.sha256(json.dumps(palette, sort_keys=True).encode()).hexdigest()
                self.assertEqual(actual, expected, 'Palette changed from approved Reef Green Dawn / Dusk baseline')
