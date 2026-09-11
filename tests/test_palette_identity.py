"""Freeze the selected Formex Dawn and original Dusk."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ithilienlib import load_palette

# Names may evolve; canonical colors, polarity and semantic assignments are frozen.
# Updating these fingerprints must accompany an explicitly intended palette change.
EXPECTED = {'dawn': 'd2271e5ff3ae960b5772261adf0e77bf2c7e158eb27813b27b1b5f7a507742ca', 'dusk': 'a9c201a636befd4d5036864ac9557eff3d6f2d5098824ac002e294df56431e90'}

class PaletteIdentity(unittest.TestCase):
    def test_selected_dawn_and_original_dusk(self):
        for variant, expected in EXPECTED.items():
            with self.subTest(variant=variant):
                palette = load_palette('ithilien-' + variant)
                palette = {k: v for k, v in palette.items() if k not in {'name', 'slug'}}
                actual = hashlib.sha256(json.dumps(palette, sort_keys=True).encode()).hexdigest()
                self.assertEqual(actual, expected, 'Palette changed from approved neutral Dawn / original Dusk baseline')
