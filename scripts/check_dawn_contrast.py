"""Check resolved native highlight pairs after check_formex_dawn.lua."""
import json
from ithilienlib import ROOT, wcag
h=json.loads((ROOT/'reports/formex-dawn-highlights.json').read_text())['highlights']
# Structural lines/whitespace have a separate 3:1 target; the Kanso helper is
# a synthetic workaround group that is never used to render user text.
structural={'FloatBorder','WinSeparator','TelescopeBorder','Whitespace','EndOfBuffer','VertSplit','NonText'}
skip={'nvim_set_hl_x_hi_clear_bugfix'}
checks=[]
for name,spec in h.items():
    if name in skip or 'fg' not in spec: continue
    fg=f'#{spec["fg"]:06X}';bg=f'#{spec.get("bg",h["Normal"]["bg"]):06X}'
    target=3 if name in structural else 4.5
    ratio=wcag(fg,bg)
    assert ratio>=target,(name,ratio,target)
    checks.append({'group':name,'ratio':round(ratio,3),'target':target})
(ROOT/'reports/formex-dawn-resolved-contrast.json').write_text(json.dumps(checks,indent=2)+'\n')
print(len(checks),'resolved foreground/background pairs pass')
