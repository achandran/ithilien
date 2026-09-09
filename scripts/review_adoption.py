"""Render the accepted parchment/black-neutral design against its pre-adoption snapshot."""
import argparse
import copy
import json
import subprocess
from unittest.mock import patch

import review_day
from explore_day_warmth import agent_panel
from ithilienlib import ROOT, load_palette, simulated_hex, wcag, delta_e

OUT = ROOT / 'reports/day-adoption'
MODES = ('normal','protan','deutan','tritan','grayscale')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--png',action='store_true')
    args=parser.parse_args()
    before=json.loads((OUT/'before.json').read_text())
    after=load_palette('ithilien-dawn')
    assert before['accents']==after['accents'], 'Unexpected syntax recoloring'
    if args.png:
        subprocess.run(['swiftc','-module-cache-path','/private/tmp/ithilien-swift-cache',
                        str(ROOT/'scripts/render_review.swift'),'-o','/private/tmp/ithilien-render-review'],check=True)
    for mode in MODES:
        for agent in ([False,True] if mode=='normal' else [False]):
            height=1020 if agent else 1080
            d=review_day.Drawing();d.rect(0,0,1540,height,'#D0CEC5')
            for x,palette,title in [(0,before,'Before / ivory and olive-charcoal'),
                                    (780,after,'Final / parchment and black neutrals')]:
                p=copy.deepcopy(palette)
                if mode!='normal':
                    for family in ('backgrounds','foregrounds','accents','ansi','diff','highlight'):
                        p[family]={k:simulated_hex(v,mode) for k,v in p[family].items()}
                if agent: agent_panel(d,p,x,title)
                else: review_day.panel(d,p,x,title,True,mode)
            stem='agent' if agent else 'code-'+mode
            with patch.object(review_day,'OUT',OUT): d.save(stem,1540,height,args.png)
    summary={
        'base':after['backgrounds']['base'],
        'neutralTextContrast':round(wcag('#000000',after['backgrounds']['base']),3),
        'syntaxRange':[round(fn(wcag(c,after['backgrounds']['base']) for c in after['accents'].values()),3) for fn in (min,max)],
        'changedLineTextContrast':round(wcag(after['diff']['changeForeground'],after['diff']['changeBackground']),3),
        'diffTextBoundary':round(wcag(after['highlight']['background'],after['diff']['changeBackground']),3),
        'changedLineCanvasDeltaEOK':{m:round(delta_e(after['diff']['changeBackground'],after['backgrounds']['base'],m),4) for m in MODES},
    }
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__': main()
