"""Compare black neutral text and all-black text without replacing the live palette.

Run python scripts/explore_black_text.py [--png].
"""
import argparse
import copy
import json
import subprocess
from unittest.mock import patch

import review_day
from explore_day_warmth import agent_panel
from ithilienlib import ROOT, load_palette, wcag

OUT = ROOT / 'reports/day-black-text'


def policy_panel(palette, policy, name, agent=False):
    p = copy.deepcopy(palette)
    if policy == 'black-neutral':
        p['foregrounds'] = {k:'#000000' for k in p['foregrounds']}
    d = review_day.Drawing()
    if agent:
        agent_panel(d, p, 0, name)
    else:
        review_day.panel(d, p, 0, name, True, 'normal')
    if policy == 'all-black':
        # Paint text black without destroying the accent tokens used as fills.
        # A real monochrome port would need this same foreground/background split.
        for command in d.commands:
            if 'text' in command:
                command['color'] = '#000000'
    return d


def save_pairs(left, right, stem, png, height):
    combined = review_day.Drawing()
    combined.rect(0,0,1540,height,'#D0CEC5')
    combined.commands.extend(left.commands)
    for original in right.commands:
        command = dict(original)
        command['x'] += 780
        combined.commands.append(command)
    with patch.object(review_day,'OUT',OUT):
        combined.save(stem,1540,height,png)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--png',action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    config=json.loads((ROOT/'experiments/day-black-text.json').read_text())
    current=json.loads((ROOT/config['referencePalette']).read_text()) if 'referencePalette' in config else load_palette('ithilien-dawn')
    warmth=json.loads((ROOT/'experiments/day-warmth.json').read_text())
    parchment=copy.deepcopy(current)
    parchment['backgrounds']=next(p['backgrounds'] for p in warmth['candidates'] if p['id']=='parchment')
    if args.png:
        subprocess.run(['swiftc','-module-cache-path','/private/tmp/ithilien-swift-cache',str(ROOT/'scripts/render_review.swift'),'-o','/private/tmp/ithilien-render-review'],check=True)
    for agent in (False,True):
        kind='agent' if agent else 'code'
        height=1020 if agent else 1080
        for policy,label in [('black-neutral','Black neutral text / colored syntax'),('all-black','All text black / colored fills')]:
            # Same background first: isolate the foreground policy.
            save_pairs(policy_panel(parchment,'current','Ithilien inks / warm parchment',agent),
                       policy_panel(parchment,policy,label,agent),policy+'-'+kind,args.png,height)
        save_pairs(policy_panel(current,'all-black','All text black / current ivory',agent),
                   policy_panel(parchment,'all-black','All text black / warm parchment',agent),
                   'black-backgrounds-'+kind,args.png,height)
    # Contrast across a broader background range, with identical dense code.
    d=review_day.Drawing()
    ratios=[]
    for i,background in enumerate(config['backgrounds']):
        p=copy.deepcopy(current);p['backgrounds']['base']=background['base']
        y=i*310
        d.rect(0,y,1000,310,background['base'])
        ratio=wcag('#000000',background['base'])
        ratios.append(dict(**background,blackContrast=round(ratio,3),
                           oliveCharcoalContrast=round(wcag(current['foregrounds']['text'],background['base']),3)))
        d.text(20,y+12,f"Black / {background['name']} {background['base']} / {ratio:.2f}:1",'#000000','bold')
        for j,line in enumerate(review_day.CODE[:9]):
            x=24
            for role,text in line:
                d.text(x,y+47+j*24,text,'#000000','italic' if role=='comment' else 'bold' if role=='clay' else 'regular')
                x+=len(text)*9
        d.text(24,y+278,'Every glyph is black; keyword weight and comment italics remain.','#000000')
    with patch.object(review_day,'OUT',OUT):
        d.save('black-background-range',1000,930,args.png)
    (OUT/'contrast.json').write_text(json.dumps(ratios,indent=2)+'\n')
    print('Wrote black-text code, agent, and background-range specimens')


if __name__=='__main__': main()
