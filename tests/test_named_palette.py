"""Named authoring must resolve faithfully and fail clearly on broken references."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ithilienlib import ROOT, ROLE_FAMILIES, load_palette, load_palette_source, resolve_palette


class NamedPalette(unittest.TestCase):
    def setUp(self):
        self.source = load_palette_source('ithilien-dawn')
        self.shared = json.loads((ROOT/'palette/ithilien-shared.json').read_text())

    def test_all_roles_use_named_colors(self):
        colors = self.source['colors']
        self.assertTrue(colors)
        references = {name for family in ROLE_FAMILIES for name in self.source[family].values()}
        self.assertEqual(references, set(colors))
        resolved = load_palette('ithilien-dawn')
        self.assertEqual(resolved['highlight']['foreground'], '#000000')
        self.assertNotIn('colors', resolved)
        self.assertNotIn('colorNotes', resolved)
        for family in ROLE_FAMILIES:
            for role, name in self.source[family].items():
                self.assertEqual(resolved[family][role], colors[name])

    def test_unknown_name_fails_with_role(self):
        self.source['foregrounds']['text'] = 'Typo'
        with self.assertRaisesRegex(ValueError, 'foregrounds.text.*Typo'):
            resolve_palette(self.shared, self.source)

    def test_duplicate_hex_aliases_are_rejected(self):
        self.source['colors']['Alias'] = self.source['colors']['Anduin']
        with self.assertRaisesRegex(ValueError, 'exactly one name'):
            resolve_palette(self.shared, self.source)

    def test_multiword_names_are_rejected(self):
        self.source['colors']['Minas Tirith'] = '#FFFFFF'
        with self.assertRaisesRegex(ValueError, 'single ASCII word'):
            resolve_palette(self.shared, self.source)

    def test_naming_does_not_mutate_sources(self):
        before = copy.deepcopy((self.shared, self.source))
        resolve_palette(self.shared, self.source)
        self.assertEqual((self.shared, self.source), before)

    def test_hex_cannot_bypass_named_authoring(self):
        self.source['foregrounds']['text'] = '#000000'
        with self.assertRaisesRegex(ValueError, 'Unknown color reference'):
            resolve_palette(self.shared, self.source)

    def test_missing_tolkien_note_is_rejected(self):
        del self.source['colorNotes']['Anduin']
        with self.assertRaisesRegex(ValueError, 'Tolkien association'):
            resolve_palette(self.shared, self.source)
