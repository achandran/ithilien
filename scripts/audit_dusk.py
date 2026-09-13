"""Dusk design contracts, measured with Tintprobe; no composite quality score."""
import json
from ithilienlib import ROOT, load_palette_source, resolve_palette, wcag, apca, delta_e

SHARED_COLORS = ('Lebethron', 'Briar', 'Heather', 'Celandine')


def assess(source):
    dawn = load_palette_source('ithilien-dawn')
    palette = resolve_palette({'colorSpace': 'sRGB'}, source)
    colors = source['colors']
    failures, checks = [], []
    if len(colors) != len(dawn['colors']) or len(set(colors.values())) != 18:
        failures.append('Dusk must use exactly 18 distinct named colors, matching Dawn')
    for name in SHARED_COLORS:
        if colors[name] != dawn['colors'][name]:
            failures.append('Shared color changed: ' + name)
    bg, fg, diff, highlight = (palette[k] for k in ('backgrounds', 'foregrounds', 'diff', 'highlight'))
    def pair(role, foreground, background, target=4.5):
        ratio = wcag(foreground, background)
        checks.append(dict(role=role, foreground=foreground, background=background,
                           contrast=round(ratio, 3), apca=round(apca(foreground, background), 2),
                           target=target, passed=ratio >= target))
        if ratio < target:
            failures.append(role)
    for surface in ('base', 'mantle', 'surface0', 'surface1', 'surface2'):
        for role, color in {**fg, **palette['accents']}.items():
            pair(role + ' on ' + surface, color, bg[surface])
    pair('reading text', fg['text'], bg['base'], 7)
    pair('selection', highlight['foreground'], highlight['background'])
    pair('search', highlight['foreground'], bg['search'])
    for kind in ('add', 'delete', 'change'):
        pair(kind + ' exact character', diff['inlineForeground'], diff[kind + 'Emphasis'], 7)
        for role, color in {**fg, **palette['accents']}.items():
            pair(kind + ' syntax ' + role, color, diff[kind + 'Background'])
    pair('conflict', diff['conflictForeground'], diff['conflictBackground'])
    for name, color in palette['ansi'].items():
        if name != 'black':
            pair('ANSI ' + name, color, bg['base'])
    return dict(status='fail' if failures else 'pass', failures=failures, checks=checks,
                color_count=len(colors), shared_colors=list(SHARED_COLORS),
                diff_separation={kind: round(delta_e(diff[kind + 'Background'], bg['base']), 4)
                                 for kind in ('add', 'delete', 'change')},
                coverage='Authored sRGB pairs only; APCA and color distance are observations. Native pixels and comfort unverified.')


def main():
    result = assess(load_palette_source('ithilien-dusk'))
    output = ROOT / 'tests/evaluation/results/palette/ithilien-dusk-audit.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(f"Dusk: {result['color_count']} colors, {len(result['checks'])} contrast checks, {result['status']}")
    if result['failures']:
        raise SystemExit(', '.join(result['failures']))


if __name__ == '__main__':
    main()
