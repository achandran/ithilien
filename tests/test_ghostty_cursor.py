"""Check actual terminal cursor exports even when applications request a block."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import generate_themes
from ithilienlib import ROOT, load_palette, wcag


def settings(path):
    return dict(line.split(' = ', 1) for line in path.read_text().splitlines()
                if ' = ' in line and not line.startswith('#'))


class GhosttyCursor(unittest.TestCase):
    def assert_readable(self, config):
        # A configured bar does not exempt its pair: applications request blocks.
        self.assertGreaterEqual(wcag(config['cursor-text'], config['cursor-color']), 4.5)

    def test_generated_and_shipped_cursor_pairs(self):
        for variant in ('dawn', 'dusk'):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as temp:
                palette = load_palette('ithilien-' + variant)
                relative = Path('ghostty/themes') / f'ithilien_{variant}.conf'
                with patch.object(generate_themes, 'ROOT', Path(temp)):
                    generate_themes.generate_ghostty(palette)
                generated = settings(Path(temp) / relative)
                self.assert_readable(generated)
                self.assertEqual(generated, settings(ROOT / relative))
                if variant == 'dawn':
                    self.assertEqual(generated['cursor-text'], palette['foregrounds']['text'])
                    self.assertEqual(generated['cursor-style'], 'block')
                    self.assertEqual(generated['cursor-color'], '#9FA9A4')
                    # User reproduced black-on-black vicmd cells with 4.5;
                    # static pair contrast alone does not cover the renderer.
                    self.assertEqual(generated['minimum-contrast'], '1')

    def test_red_bar_does_not_exempt_unreadable_block_pair(self):
        with self.assertRaises(AssertionError):
            self.assert_readable({'cursor-style': 'bar', 'cursor-text': '#25292B',
                                  'cursor-color': '#A3373E'})
