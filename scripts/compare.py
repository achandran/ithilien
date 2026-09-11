#!/usr/bin/env python3
"""Prepare isolated Ghostty comparisons, or print identical ANSI scenarios."""
import argparse
from pathlib import Path
import shlex
import sys
ROOT = Path(__file__).resolve().parents[1]
SOURCES = {'dawn': ROOT/'ghostty/themes/ithilien_dawn.conf',
           'pearl': ROOT/'comparison/upstream/kanso-pearl.conf',
           'zenbones': ROOT/'comparison/upstream/zenbones-light.conf'}


def prepare():
    out = ROOT / 'comparison/generated'
    out.mkdir(parents=True, exist_ok=True)
    for name, source in SOURCES.items():
        # Compare upstream colors, with identical typography and renderer settings.
        lines = [line for line in source.read_text().splitlines() if not any(line.startswith(k) for k in ('font-', 'window-title-font-family', 'minimum-contrast', 'faint-opacity', 'cursor-style'))]
        lines += ['font-family = Berkeley Mono Medium', 'window-title-font-family = Berkeley Mono Medium',
                  'font-size = 14', 'font-thicken = false', 'minimum-contrast = 1',
                  'faint-opacity = 1', 'cursor-style = block', f'title = Ithilien comparison: {name}']
        # Kanso omits cursor-text upstream; explicitly reproduce its light canvas
        # to avoid inheriting Dawn text if a user loads this as a theme.
        if name == 'pearl':
            lines.append('cursor-text = #f2f1ef')
        config = out / f'{name}.conf'
        config.write_text('\n'.join(lines)+'\n')
        args = f'--config-default-files=false --config-file={shlex.quote(str(config))}'
        print(f'{name} — macOS: open -na Ghostty --args {args}')
        print(f'{name} — Linux: ghostty {args}')
    print('Inside each window, run: python3 ' + shlex.quote(str(ROOT/'scripts/compare.py')) + ' --scenario')


def scenarios():
    esc='\033['
    def color(n, text): return f'{esc}38;5;{n}m{text}{esc}0m'
    print('IDENTICAL ANSI SPECIMEN — not native Neovim or agent rendering\n')
    print('1. Palette / punctuation / identifiers')
    for n in range(16): print(color(n, f'{n:2}: Aa 0O 1lI [] {{}} != -> /_'), end='  \n')
    print('\n2. Prompt: explicit black versus terminal default')
    print(color(0,'anand')+'@'+color(13,'nemesis')+':'+color(4,'~/src')+' '+color(5,'main')+'\n$ git diff')
    print('anand@'+color(13,'nemesis')+':'+color(4,'~/src')+' '+color(5,'main')+'\n$ git diff')
    print('\n3. Code (fixed ANSI mapping across themes)')
    print(color(8,'# Retry transient failures; preserve cancellation'))
    print(color(5,'def')+' '+color(4,'fetch')+'(url, retries='+color(3,'3')+'):')
    print('    '+color(5,'return')+' client.get(url, timeout='+color(3,'30_000')+')')
    print('\n4. Diff: same foreground roles; stronger spans use bold + underline')
    for sign, number, value in [('-',1,'3'),('+',2,'6')]:
        print(color(number,sign+' timeout = '+esc+'1;4m'+value+esc+'22;24m'+'0_000'))
    print(color(1,'- if retries < 3:')); print(color(2,'+ if retries <'+esc+'1;4m'+'='+esc+'22;24m'+' 3:'))
    print('\n5. Agent-like prose, not an actual agent screenshot')
    print(color(2,'✓ Tests passed')+'  '+color(3,'! Retry pending')+'  '+color(1,'× Request failed'))
    print(esc+'2mDimmed context: deleted token / existing code'+esc+'0m')
    print('Read long text; drag-select across colored words and punctuation.')
    print('\n6. Native cursor: at your normal zsh prompt, type without executing:')
    print('echo userChrome.css timeout=30_000 retries=3')
    print('Press Escape, move with h/l, select with v, return with i. Check each glyph.')
    print('\n7. Native apps: repeat the same file/diff in Neovim and real agent output.')
    print('Terminal palettes do not replace explicit truecolor emitted by those apps.')


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--scenario',action='store_true');a=p.parse_args()
    scenarios() if a.scenario else prepare()
