"""Shared color and palette helpers for Ithilien."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tintprobe.colors import Color


ROOT = Path(__file__).resolve().parent.parent
PALETTE_DIR = ROOT / "palette"
PALETTE_PATH = PALETTE_DIR / "ithilien-dusk.json"
SHARED_PATH = PALETTE_DIR / "ithilien-shared.json"


ROLE_FAMILIES = ('backgrounds', 'foregrounds', 'accents', 'ansi', 'diff', 'highlight')


def load_palette_source(variant: str) -> dict:
    """Read authored names and role references, before resolving to sRGB."""
    return json.loads((PALETTE_DIR / f"{variant}.json").read_text())


def resolve_palette(shared: dict, specific: dict) -> dict:
    """Resolve named colors while retaining the existing integration contract."""
    palette = {**shared, **specific}
    colors = palette.pop('colors', {})
    notes = palette.pop('colorNotes', {})
    if colors:
        for name, color in colors.items():
            if not re.fullmatch(r'[A-Z][a-z]+', name):
                raise ValueError(f'Color name must be a single ASCII word: {name!r}')
            if not isinstance(color, str) or not re.fullmatch(r'#[0-9A-F]{6}', color):
                raise ValueError(f'Invalid sRGB color for {name}: {color!r}')
        if len(set(colors.values())) != len(colors):
            raise ValueError('Each distinct color must have exactly one name')
        if set(notes) != set(colors):
            raise ValueError('Every named color needs a Tolkien association and source')
        for name, note in notes.items():
            if not note.get('meaning') or not note.get('source', '').startswith('https://'):
                raise ValueError(f'Missing Tolkien association/source for {name}')
    used = set()
    for family in ROLE_FAMILIES:
        resolved = {}
        for role, value in palette[family].items():
            if value in colors:
                used.add(value)
                resolved[role] = colors[value]
            elif not colors and re.fullmatch(r'#[0-9A-Fa-f]{6}', value):
                resolved[role] = value
            else:
                raise ValueError(f'Unknown color reference {family}.{role}: {value!r}')
        palette[family] = resolved
    if colors and used != set(colors):
        raise ValueError(f'Unused named colors: {sorted(set(colors) - used)}')
    return palette


def load_palette(variant: str = "ithilien-dusk") -> dict:
    """Return resolved role-to-hex pairs, excluding authoring metadata."""
    shared = json.loads(SHARED_PATH.read_text())
    return resolve_palette(shared, load_palette_source(variant))


# Public compatibility imports for the theme generator and policy tests.
from tintprobe.colors import rgb, wcag, apca, oklch, delta_e, simulated_hex
