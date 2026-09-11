"""Generate matched, annotated Day specimens (SVG, HTML, and optional macOS PNG).

These are controlled role specimens, not screenshots of an application.
Run: python scripts/review_day.py [--png]
"""
import argparse
import copy
import html
import json
import subprocess
import tempfile
from pathlib import Path
from ithilienlib import ROOT, load_palette, simulated_hex, wcag

OUT = ROOT / 'reports/day-review'
CODE = [
 [('comment','// Resolve retries without hiding partial failures.')],
 [('clay','export type '),('aqua','RetryPolicy'),('text',' = { limit: '),('aqua','number'),('text','; delay: '),('aqua','number'),('text',' }')],
 [('clay','const '),('text','policy: '),('aqua','RetryPolicy'),('text',' = { limit: '),('ochre','3'),('text',', delay: '),('ochre','250'),('text',' }')],
 [('clay','export async function '),('gold','fetchWithRetry'),('text','(url: '),('aqua','string'),('text',') {')],
 [('text','  '),('clay','for '),('text','('),('clay','let '),('text','attempt = '),('ochre','0'),('text','; attempt '),('olive','< '),('text','policy.limit; attempt'),('olive','++'),('text',') {')],
 [('text','    '),('clay','const '),('text','response = '),('clay','await '),('gold','fetch'),('text','(url, { cache: '),('sage','"no-store"'),('text',' })')],
 [('text','    '),('clay','if '),('text','(response.status '),('olive','=== '),('ochre','429'),('text',') {')],
 [('text','      '),('clay','await '),('gold','sleep'),('text','(policy.delay '),('olive','* '),('text','(attempt '),('olive','+ '),('ochre','1'),('text','))')],
 [('text','      '),('clay','continue')],
 [('text','    }')],
 [('text','    '),('clay','if '),('text','('),('olive','!'),('text','response.ok) '),('clay','throw new '),('aqua','Error'),('text','('),('sage','"request failed"'),('text',')')],
 [('text','    '),('clay','return '),('text','response.'),('gold','json'),('text','() '),('clay','as '),('aqua','Promise<Result>')],
 [('text','  }')],
 [('text','  '),('clay','throw new '),('aqua','Error'),('text','('),('sage','"retry budget exhausted"'),('text',')')],
 [('text','}')],
 [('mauve','describe'),('text','('),('sage','"retries"'),('text',', () '),('olive','=> '),('gold','expect'),('text','(policy.limit).'),('gold','toBe'),('text','('),('ochre','3'),('text','))')],
]

class Drawing:
    def __init__(self): self.commands=[]
    def rect(self,x,y,w,h,color): self.commands.append(dict(x=x,y=y,w=w,h=h,color=color))
    def text(self,x,y,text,color,style='regular'): self.commands.append(dict(x=x,y=y,text=text,color=color,style=style))
    def save(self, stem, width, height, png):
        svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<style>text{font-family:"Berkeley Mono Medium",monospace;font-size:16pt}</style>']
        for c in self.commands:
            if 'text' in c:
                style='font-weight="700" font-style="italic"' if c['style']=='bold-italic' else 'font-weight="700"' if c['style']=='bold' else 'font-style="italic"' if c['style']=='italic' else ''
                svg.append(f'<text x="{c["x"]}" y="{c["y"]+15}" fill="{c["color"]}" {style}>{html.escape(c["text"])}</text>')
            else: svg.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" fill="{c["color"]}"/>')
        (OUT/f'{stem}.svg').write_text('\n'.join(svg+['</svg>']))
        if png:
            with tempfile.NamedTemporaryFile(suffix='.json',mode='w') as f:
                json.dump(dict(width=width,height=height,commands=self.commands),f);f.flush()
                subprocess.run(['/private/tmp/ithilien-render-review',f.name,str(OUT/f'{stem}.png')],check=True)

def panel(d,p,x,title,revised,mode):
    b,f,a,df=p['backgrounds'],p['foregrounds'],p['accents'],p['diff']; c={**f,**a}
    d.rect(x,0,760,1080,b['base']);d.rect(x,0,760,42,b['crust']);d.text(x+18,12,title,f['text'],'bold')
    d.rect(x,42,760,32,b['mantle']);d.text(x+18,49,'src/retry.ts   |   main   |   UTF-8',f['subtext'])
    for i,line in enumerate(CODE):
        y=86+i*23
        if i==7: d.rect(x,y-1,760,23,b['surface1'])
        d.text(x+15,y,f'{i+1:2}',f['muted']);pos=x+52
        for role,text in line:
            d.text(pos,y,text,c[role],'italic' if role=='comment' else 'bold' if role=='clay' and revised else 'regular');pos+=len(text)*9
    for i,(label,role) in enumerate([('E  Error: Result is not defined','coral'),('W  Warning: retry may repeat a side effect','gold'),('I  Info: response body is parsed as JSON','blue'),('H  Hint: extract a named delay constant','aqua')]):
        y=466+i*24;d.rect(x+12,y,736,24,b['surface0']);d.text(x+22,y+2,label,a[role])
    d.rect(x+16,578,360,114,f['muted'] if revised else b['surface2']);d.rect(x+17,579,358,112,b['surface0'])
    d.text(x+28,584,'Completion / documentation',f['subtext'])
    d.text(x+28,610,'fetchWithRetry    (function)',a['gold'])
    d.rect(x+18,636,356,25,p['highlight']['background']);d.text(x+28,639,'fetch',p['highlight']['foreground']);d.text(x+181,639,'[web]',p['highlight']['foreground'] if revised else f['subtext'])
    d.text(x+28,668,'// Returns a parsed response',f['comment'],'italic')
    d.text(x+398,580,'Interaction comparison',f['subtext'])
    d.rect(x+398,609,344,26,p['highlight']['background']);d.text(x+405,613,' selected text: 5.32:1 ',p['highlight']['foreground'])
    d.rect(x+398,647,344,26,p['highlight']['background'] if revised else df['changeEmphasis']);d.text(x+405,651,' search match ',p['highlight']['foreground'] if revised else f['text'])
    d.rect(x,711,760,31,b['mantle']);d.text(x+18,717,'diff --git a/retry.ts b/retry.ts',f['subtext'])
    rows=[('hunk','@@ -3,4 +3,4 @@ retry policy',None),('delete','- const limit = 2','2'),('add','+ const limit = 3','3'),('delete','- if (ready && valid) {','&&'),('add','+ if (ready || valid) {','||'),('change','~ // Preserve partial failures','partial failures'),('conflict','! <<<<<<< current / incoming',None)]
    for i,(state,text,em) in enumerate(rows):
        y=750+i*26;d.rect(x,y,760,26,df[state+'Background']);d.text(x+18,y+3,text,df[state+'Foreground'])
        if em:
            j=text.index(em);ex=x+18+j*9
            # Neovim DiffText is the changed-line inline state.
            eb=df[state+'Emphasis'];ef=df['inlineForeground']
            if state=='change': eb=p['highlight']['background'];ef=p['highlight']['foreground']
            d.rect(ex,y,len(em)*9,26,eb);d.text(ex,y+3,em,ef,'bold')
            if revised and state != 'change': d.rect(ex,y+23,len(em)*9,1,ef)
    d.text(x+18,951,'Terminal: all 16 ANSI foregrounds on the canvas',f['subtext'])
    for i,(name,color) in enumerate(list(p['ansi'].items())[:16]):
        d.text(x+18+(i%8)*92,978+(i//8)*24,f'{i:02} Aa1',color)
    d.rect(x,1039,760,41,b['mantle']);d.text(x+18,1050,'inactive: retry.ts   16 lines   no pending changes',f['muted'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--png',action='store_true');args=ap.parse_args()
    if args.png: subprocess.run(['swiftc','-module-cache-path','/private/tmp/ithilien-swift-cache',str(ROOT/'scripts/render_review.swift'),'-o','/private/tmp/ithilien-render-review'],check=True)
    before={**load_palette('ithilien-dawn'),**json.loads((OUT/'before.json').read_text())};after=load_palette('ithilien-dawn')
    contrasts=[]
    for name,token,surface in [('Main text','text','base'),('Secondary text','subtext','base'),
                               ('Comments','comment','base'),('Muted labels','muted','base'),
                               ('Comments on mantle','comment','mantle'),
                               ('Comments on active line','comment','surface1'),
                               ('Inactive status label','muted','mantle')]:
        contrasts.append(dict(role=name, **{label:round(wcag(p['foregrounds'][token],p['backgrounds'][surface]),3)
                                            for label,p in [('before',before),('after',after)]}))
    (OUT/'contrast-comparison.json').write_text(json.dumps(contrasts,indent=2)+'\n')
    for mode in ['normal','protan','deutan','tritan','grayscale']:
        d=Drawing()
        for x,p,title,rev in [(0,before,'BEFORE / 1db45d5',False),(780,after,'AFTER / Ithilien Dawn',True)]:
            p=copy.deepcopy(p)
            if mode!='normal':
                for family in ['backgrounds','foregrounds','accents','diff','ansi','highlight']:
                    p[family]={k:simulated_hex(v,mode) for k,v in p[family].items()}
            panel(d,p,x,title+' / '+mode,rev,mode)
        d.save('comparison-'+mode,1540,1080,args.png)
    benchmarks=json.loads((OUT/'benchmarks.json').read_text())
    roles={'string':'sage','keyword':'clay','function':'gold','type':'aqua','number':'ochre'}
    own=dict(name='Ithilien Dawn (revised)',background=after['backgrounds']['base'],
             text=after['foregrounds']['text'],comment=after['foregrounds']['comment'],
             **{k:after['accents'][v] for k,v in roles.items()})
    d=Drawing();rows=[]
    for i,p in enumerate([own]+benchmarks):
        x=(i%2)*780;y=(i//2)*500
        d.rect(x,y,760,480,p['background']);d.text(x+16,y+12,p['name'],p['text'],'bold')
        colors={**after['accents'],**after['foregrounds'],'text':p['text'],'comment':p['comment'],
                **{v:p[k] for k,v in roles.items()},'olive':p['text'],'mauve':p['function']}
        for j,line in enumerate(CODE):
            pos=x+16
            for role,text in line:
                d.text(pos,y+48+j*23,text,colors[role],'italic' if role=='comment' else 'regular');pos+=len(text)*9
        ratios={k:round(wcag(p[k],p['background']),2) for k in ['text','comment',*roles]}
        rows.append(dict(name=p['name'],ratios=ratios))
        d.text(x+16,y+433,f"Text {ratios['text']}:1 / comment {ratios['comment']}:1",p['text'])
    d.save('benchmarks',1540,1480,args.png)
    (OUT/'benchmark-contrast.json').write_text(json.dumps(rows,indent=2)+'\n')
    (OUT/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Ithilien Dawn review</title>
<style>body{font:16px system-ui;background:#eee;margin:24px}img{width:100%;height:auto}a{margin-right:18px}</style>
<h1>Ithilien Dawn: matched role specimens</h1><p>Berkeley Mono, 15 px, identical code and geometry. Controlled specimens, not application screenshots. Left: 1db45d5. Right: revised Day. Selection and DiffText preserve black foregrounds. Selection ratio labels refer to normal vision. Simulations use Machado severity 1; grayscale uses the repository filter.</p>
<nav>'''+''.join(f'<a href="#'+m+'">'+m+'</a>' for m in ['normal','protan','deutan','tritan','grayscale'])+'</nav><p><a href="benchmarks.svg">Comparison palette specimens</a> (representative token selections; not native editor ports).</p>'+''.join(f'<h2 id="{m}">{m}</h2><img src="comparison-{m}.svg" alt="Before and after Day under {m}">' for m in ['normal','protan','deutan','tritan','grayscale']))

if __name__=='__main__': main()
