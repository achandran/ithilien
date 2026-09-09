"""Protect the exact pre-rename colors and role assignments from commit 2ec16c0."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ithilienlib import load_palette

# Names may evolve; canonical colors, polarity and semantic assignments are frozen.
# Updating these fingerprints must accompany an explicitly intended palette change.
EXPECTED = {'dawn': '87de8b1e8f4b98312648fad7a9c2c930e98a1a97ca32bef8324556d91094b698', 'dusk': 'a9c201a636befd4d5036864ac9557eff3d6f2d5098824ac002e294df56431e90'}

class PaletteIdentity(unittest.TestCase):
    def test_rename_preserves_both_palettes(self):
        for variant, expected in EXPECTED.items():
            with self.subTest(variant=variant):
                palette = load_palette('ithilien-' + variant)
                palette = {k: v for k, v in palette.items() if k not in {'name', 'slug'}}
                actual = hashlib.sha256(json.dumps(palette, sort_keys=True).encode()).hexdigest()
                self.assertEqual(actual, expected, 'Palette or semantic role changed since 2ec16c0')
