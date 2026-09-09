"""Render matched Day refinement specimens; historical reviews stay frozen."""
import argparse
import copy
import json
import subprocess
from unittest.mock import patch
import review_day
from explore_day_warmth import agent_panel
from ithilienlib import ROOT, load_palette, simulated_hex, wcag

OUT=ROOT/'reports/day-refinement'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--png',action='store_true')
    args=parser.parse_args()
    before=json.loads((OUT/'before.json').read_text());after=load_palette('ithilien-dawn')
    if args.png:
        subprocess.run(['swiftc','-module-cache-path','/private/tmp/ithilien-swift-cache',str(ROOT/'scripts/render_review.swift'),'-o','/private/tmp/ithilien-render-review'],check=True)
    for mode in ['normal','protan','deutan','tritan','grayscale']:
        for agent in ([False,True] if mode=='normal' else [False]):
            h=1020 if agent else 1080
            d=review_day.Drawing();d.rect(0,0,1540,h,'#D0CEC5')
            for x,original,title,new in [(0,before,'Before / 94e7c31',False),(780,after,'Refined / black main text, readable hierarchy',True)]:
                p=copy.deepcopy(original)
                if mode!='normal':
                    for family in ['backgrounds','foregrounds','accents','diff','ansi','highlight']:
                        p[family]={k:simulated_hex(v,mode) for k,v in p[family].items()}
                if agent:agent_panel(d,p,x,title)
                else:
                    review_day.panel(d,p,x,title,True,mode)
                    if new:
                        # The active number has weight and foreground distinction.
                        d.rect(x+12,246,31,25,p['backgrounds']['surface1'])
                        d.text(x+15,247,' 8',p['foregrounds']['text'],'bold')
                    # Light ANSI foregrounds are used on dark indexed backgrounds.
                    b=p['backgrounds'];f=p['foregrounds']
                    d.rect(x,944,760,92,b['base'])
                    d.text(x+18,948,'ANSI: canvas text / light endpoints on black',f['subtext'])
                    for i,(name,color) in enumerate(list(p['ansi'].items())[:16]):
                        xx=x+18+(i%8)*92;yy=978+(i//8)*24
                        d.rect(xx-2,yy-1,85,23,p['ansi']['black'] if name in ['white','brightWhite'] else b['base'])
                        d.text(xx,yy,f'{i:02} Aa1',color)
            with patch.object(review_day,'OUT',OUT):d.save('agent' if agent else 'code-'+mode,1540,h,args.png)
    # Direct comparison of the previously failing composition and secondary text
    # without italics, as in renderers that suppress theme italics.
    d=review_day.Drawing();d.rect(0,0,1540,660,'#D0CEC5')
    for x,p,title in [(0,before,'Before / 94e7c31'),(780,after,'Refined / palette composition')]:
        b,f,a,df=(p[k] for k in ['backgrounds','foregrounds','accents','diff'])
        d.rect(x,0,760,660,b['base']);d.text(x+18,15,title,f['text'],'bold')
        d.text(x+18,57,'Main prose stays black and crisp.',f['text'])
        d.text(x+18,85,'// Comments remain distinct without italics.',f['comment'])
        d.text(x+18,113,'Secondary details: 24 lines, 2 changes',f['subtext'])
        for i,state in enumerate(['add','delete']):
            y=161+i*150;d.rect(x+12,y,736,138,df[state+'Background'])
            d.text(x+22,y+8,state.title()+' line with syntax foregrounds',f['text'],'bold')
            for j,line in enumerate(review_day.CODE[2:4]):
                pos=x+22
                for role,txt in line:
                    d.text(pos,y+39+j*25,txt,{**f,**a}[role],'bold' if role=='clay' else 'regular');pos+=len(txt)*9
            d.text(x+22,y+104,'Number contrast: '+str(round(wcag(a['ochre'],df[state+'Background']),2))+':1',f['text'])
        d.text(x+18,479,'Indexed white on black: SGR 37;40',f['subtext'])
        d.rect(x+18,510,724,32,p['ansi']['black']);d.text(x+28,517,'Readable status text',p['ansi']['white'])
        d.text(x+18,567,'Matched 15 px Berkeley Mono; controlled role specimen.',f['subtext'])
        d.text(x+18,595,'Revised Ghostty: faint text stays opaque; minimum contrast 4.5:1.' if x else 'Previous Ghostty: host dimming was not controlled by this theme.',f['subtext'])
    with patch.object(review_day,'OUT',OUT):d.save('composition',1540,660,args.png)
    summary={label:{
        'text':wcag(p['foregrounds']['text'],p['backgrounds']['base']),
        'comment':wcag(p['foregrounds']['comment'],p['backgrounds']['base']),
        'subtext':wcag(p['foregrounds']['subtext'],p['backgrounds']['base']),
        'diffSyntaxMinimum':{s:min(wcag(v,p['diff'][s+'Background']) for v in p['accents'].values()) for s in ['add','delete','change']},
        'inlineFillContrast':{s:wcag(p['diff'][s+'Emphasis'],p['diff'][s+'Background']) for s in ['add','delete','change']},
        'ansiWhiteOnBlack':wcag(p['ansi']['white'],p['ansi']['black']),
    } for label,p in [('before',before),('after',after)]}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
