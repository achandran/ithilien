"""Check resolved native highlight pairs after check_highlights.lua."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ithilienlib import ROOT, wcag
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=ROOT/'tests/results/highlight-checks')
args = parser.parse_args()
h=json.loads((args.output/'highlights.json').read_text())['highlights']
# Structural lines/whitespace have a separate 3:1 target; the highlight helper is
# a synthetic workaround group that is never used to render user text.
structural={'IthilienDiffFiller','FloatBorder','WinSeparator','TelescopeBorder','Whitespace','EndOfBuffer','VertSplit','NonText'}
# Decorative indent guides are palette-role assertions, not ordinary text.
guides={'SnacksIndent','IblIndent','IndentBlanklineChar','NeoTreeIndentMarker'}
skip={'nvim_set_hl_x_hi_clear_bugfix'}
from ithilienlib import load_palette
guide_color=int(load_palette('ithilien-dawn')['backgrounds']['surface2'][1:],16)
checks=[]
for name,spec in h.items():
    if name in skip or 'fg' not in spec: continue
    if name in guides:
        assert spec['fg']==guide_color,(name, 'indent guide palette role')
        continue
    fg=f'#{spec["fg"]:06X}';bg=f'#{spec.get("bg",h["Normal"]["bg"]):06X}'
    target=3 if name in structural else 4.5
    ratio=wcag(fg,bg)
    assert ratio>=target,(name,ratio,target)
    checks.append({'group':name,'ratio':round(ratio,3),'target':target})
(args.output/'resolved-contrast.json').write_text(json.dumps(checks,indent=2)+'\n')
print(len(checks),'resolved foreground/background pairs pass')
