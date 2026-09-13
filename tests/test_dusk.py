"""Contracts for the new 18-color Dusk and its exported interaction pairs."""
import copy
import json
import plistlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ithilienlib import ROOT, ROLE_FAMILIES, load_palette, load_palette_source
from audit_dusk import assess, SHARED_COLORS


def test_dusk_matches_dawn_color_budget_and_shared_interactions():
    dawn, dusk = (load_palette_source('ithilien-' + v) for v in ('dawn', 'dusk'))
    assert len(dusk['colors']) == len(dawn['colors']) == 18
    assert len(set(dusk['colors'].values())) == 18
    assert {value for family in ROLE_FAMILIES for value in dusk[family].values()} == set(dusk['colors'])
    for name in SHARED_COLORS:
        assert dusk['colors'][name] == dawn['colors'][name]
    p = load_palette('ithilien-dusk')
    assert p['highlight']['foreground'] == p['diff']['inlineForeground'] == '#000000'
    assert p['highlight']['background'] == p['highlight']['cursorBlock'] == '#B8595C'
    assert p['backgrounds']['search'] == '#D6C6DE'
    for kind in ('add', 'delete', 'change'):
        assert p['diff'][kind + 'Emphasis'] == '#D8B46A'


def test_dusk_reading_and_diff_pairs_pass():
    assert assess(load_palette_source('ithilien-dusk'))['failures'] == []


def test_audit_rejects_unreadable_comments_and_changed_shared_color():
    source = copy.deepcopy(load_palette_source('ithilien-dusk'))
    source['colors'][source['foregrounds']['comment']] = '#353535'
    assert 'comment on base' in assess(source)['failures']
    source = copy.deepcopy(load_palette_source('ithilien-dusk'))
    source['colors']['Briar'] = '#B95A5D'
    assert 'Shared color changed: Briar' in assess(source)['failures']


def test_dusk_exports_preserve_interactions_and_diff_roles():
    p = load_palette('ithilien-dusk')
    ghostty = (ROOT / 'extras/ghostty/themes/ithilien_dusk.conf').read_text()
    assert 'cursor-color = #B8595C\ncursor-text = #000000' in ghostty
    assert 'selection-background = #B8595C\nselection-foreground = #000000' in ghostty
    assert 'minimum-contrast = 1' in ghostty
    assert 'font-family = Berkeley Mono Retina' in ghostty
    assert 'font-size = 16' in ghostty
    with (ROOT / 'extras/codex/themes/ithilien-dusk.tmTheme').open('rb') as f:
        rules = plistlib.load(f)['settings']
    assert rules[0]['settings']['selectionForeground'] == '#000000'
    for label, kind in [('Inserted diff', 'add'), ('Deleted diff', 'delete')]:
        spec = next(r['settings'] for r in rules if r.get('name') == label)
        assert spec['background'] == p['diff'][kind + 'Background']
        assert spec['foreground'] == p['foregrounds']['text']
    claude = json.loads((ROOT / 'extras/claude-code/themes/ithilien-dusk.json').read_text())
    assert claude['base'] == 'dark'
    assert claude['overrides']['diffAddedWord'] == '#D8B46A'
    assert claude['overrides']['diffRemovedWord'] == '#D8B46A'


def test_ansi_regular_and_bright_accents_share_colors():
    ansi = load_palette('ithilien-dusk')['ansi']
    for name in ('red', 'green', 'yellow', 'blue', 'magenta', 'cyan'):
        assert ansi[name] == ansi['bright' + name.capitalize()]


def test_selected_fzf_pointer_pair_uses_selection_background():
    from check_dusk_interactions import fzf_roles
    options = '--color=dark,bg:#202120,bg+:#B8595C,fg+:#000000,pointer:#000000,gutter:#202120'
    assert fzf_roles(options)['pointer']['pass']
    assert not fzf_roles(options.replace('pointer:#000000', 'pointer:#BDB7AB'))['pointer']['pass']


def test_palette_names_identify_one_exact_color_across_variants():
    dawn, dusk = (load_palette_source('ithilien-' + v)['colors'] for v in ('dawn', 'dusk'))
    assert dawn.keys() & dusk.keys() == set(SHARED_COLORS)
    names, colors = {}, {}
    for palette in (dawn, dusk):
        for name, color in palette.items():
            assert names.setdefault(name, color) == color
            assert colors.setdefault(color, name) == name


def test_dusk_surface_roles_have_distinct_purposes():
    backgrounds = load_palette_source('ithilien-dusk')['backgrounds']
    assert backgrounds['base'] == 'Duath'
    assert backgrounds['surface0'] == backgrounds['surface1'] == 'Arnen'
    assert backgrounds['mantle'] == backgrounds['surface2'] == 'Morgai'


def test_dusk_and_dawn_define_the_same_functional_roles():
    dawn, dusk = (load_palette_source('ithilien-' + v) for v in ('dawn', 'dusk'))
    assert dawn.keys() == dusk.keys()
    for family in ROLE_FAMILIES:
        assert dawn[family].keys() == dusk[family].keys(), family
