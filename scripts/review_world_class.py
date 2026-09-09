"""Reproduce the independent Day assessment; does not edit production themes.

Run: .venv/bin/python scripts/review_world_class.py [--png]
Optional: --kanso /path/to/kanso.nvim captures selected resolved highlight groups.
"""
import argparse
import json
import subprocess
import tempfile
from itertools import combinations
from pathlib import Path

import review_day
from lodenlib import ROOT, delta_e, load_palette, oklch, simulated_hex, wcag

OUT = ROOT / 'reports/day-deep-dive'
MODES = ['normal', 'protan', 'deutan', 'tritan', 'grayscale']


def independent_contrast(first, second):
    def luminance(value):
        channels = [int(value[i:i+2], 16)/255 for i in (1, 3, 5)]
        linear = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in channels]
        return sum(c*w for c, w in zip(linear, (.2126, .7152, .0722)))
    lo, hi = sorted([luminance(first), luminance(second)])
    return (hi+.05)/(lo+.05)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--png', action='store_true')
    parser.add_argument('--kanso', type=Path)
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    review_day.OUT = OUT
    if args.png:
        subprocess.run(['swiftc', '-module-cache-path', '/private/tmp/loden-swift-cache',
                        str(ROOT/'scripts/render_review.swift'), '-o', '/private/tmp/loden-render-review'], check=True)
    p = load_palette('loden-day')
    b, a, f, df = (p[k] for k in ('backgrounds', 'accents', 'foregrounds', 'diff'))
    all_colors = [v for k in ('backgrounds','accents','foregrounds','ansi','diff','highlight') for v in p[k].values()]
    error = max(abs(wcag(x,y)-independent_contrast(x,y)) for x,y in combinations(all_colors,2))
    # ColorAide uses higher-precision sRGB luminance coefficients than the
    # rounded WCAG reference formula. Record the discrepancy and compare gates.
    audit=json.loads((ROOT/'reports/loden-day-audit.json').read_text())
    gate_agreement=all((independent_contrast(q['foreground'],q['background']) >= q['wcagTarget']) ==
                       (wcag(q['foreground'],q['background']) >= q['wcagTarget']) for q in audit['contrast'])
    assert gate_agreement
    roles = {'string':'sage','keyword':'clay','function':'gold','type':'aqua','number':'ochre'}
    own = dict(name='Loden Day / 4289246', background=b['base'], text=f['text'], comment=f['comment'],
               **{k:a[v] for k,v in roles.items()})
    benchmarks = json.loads((ROOT/'reports/day-review/benchmarks.json').read_text())
    benchmarks[1]['name'] = 'Ef Day / pinned e1f6176'
    gruvbox = dict(name='Gruvbox Light Soft / original',
                   source='https://github.com/morhetz/gruvbox/blob/master/colors/gruvbox.vim',
                   background='#F2E5BC', text='#3C3836', comment='#928374', string='#79740E',
                   keyword='#9D0006', function='#79740E', type='#B57614', number='#8F3F71')
    comparisons = [own, gruvbox, *benchmarks]
    result = dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                  method='Opaque sRGB; WCAG recomputed with independent piecewise transfer formula. CVD uses repository Machado severity 1; distances are observations.',
                  maximumContrastFormulaDifference=error,
                  independentWcagGateAgreement=gate_agreement,
                  benchmarks=[dict(**q, ratios={k:round(independent_contrast(q[k],q['background']),4)
                                               for k in ['text','comment',*roles]}) for q in comparisons],
                  surfaces=[dict(token=k,hex=v,oklch=oklch(v),canvasContrast=wcag(v,b['base']),
                                 canvasDeltaEOK=delta_e(v,b['base'])) for k,v in b.items()],
                  semanticPairs=[dict(pair=f'{x}/{y}', distances={m:delta_e(a[x],a[y],m) for m in MODES})
                                 for x,y in [('ochre','clay'),('blue','aqua'),('sage','aqua'),('olive','ochre'),('gold','ochre')]],
                  inline=[dict(state=s,foregroundContrast=wcag(df['inlineForeground'],df[s+'Emphasis']),
                               fillLineContrast=wcag(df[s+'Emphasis'],df[s+'Background']),
                               distances={m:delta_e(df[s+'Emphasis'],df[s+'Background'],m) for m in MODES})
                          for s in ['add','delete','change']],
                  conditionalSyntaxOverlays=[dict(surface=s,role=k,ratio=wcag(v,df[s+'Background']))
                                             for s in ['add','delete','change'] for k,v in a.items()],
                  ansiExamples=[dict(sequence=seq,foreground=p['ansi'][x],background=p['ansi'][y],
                                     ratio=wcag(p['ansi'][x],p['ansi'][y]))
                                for seq,x,y in [('37;40','white','black'),('30;47','black','white'),
                                               ('97;40','brightWhite','black'),('37;41','white','red')]])
    if args.kanso:
        from check_neovim import capture
        with tempfile.TemporaryDirectory() as t:
            h=capture(ROOT,args.kanso.resolve(),'day',Path(t))
        names=['Normal','Comment','LineNr','CursorLineNr','StatusLine','StatusLineNC','Search','IncSearch',
               'CurSearch','Visual','DiffText','GitSignsAddInline','GitSignsDeleteInline','GitSignsChangeInline',
               'DiagnosticUnderlineInfo','DiagnosticUnderlineHint']
        result['resolvedHighlights']={k:h[k] for k in names}
        result['kansoCommit']=subprocess.check_output(['git','-C',str(args.kanso),'rev-parse','HEAD'],text=True).strip()
    (OUT/'measurements.json').write_text(json.dumps(result,indent=2)+'\n')
    # Same code, font and size. Representative palette roles, not native theme comparisons.
    d=review_day.Drawing();d.rect(0,0,1540,1825,'#FFFFFF')
    for i,q in enumerate(comparisons):
        x=(i%2)*780;y=(i//2)*460
        d.rect(x,y,760,445,q['background']);d.text(x+16,y+10,q['name'],q['text'],'bold')
        colors={**a,**f,'text':q['text'],'comment':q['comment'],**{v:q[k] for k,v in roles.items()},
                'olive':q['text'],'mauve':q['function']}
        if i==0: colors.update(olive=a['olive'],mauve=a['mauve'])
        for j,line in enumerate(review_day.CODE):
            pos=x+16
            for role,text in line:
                style='italic' if role=='comment' else 'bold' if i==0 and role=='clay' else 'bold' if i==1 and role=='gold' else 'regular'
                d.text(pos,y+44+j*23,text,colors[role],style);pos+=len(text)*9
    d.save('comparison',1540,1825,args.png)
    d=review_day.Drawing();d.rect(0,0,1100,700,b['base'])
    d.text(24,18,'Syntax colors on diff fills / source-derived composition',f['text'],'bold')
    for i,(title,background) in enumerate([('Canvas',b['base']),('Added line',df['addBackground']),('Deleted line before host dimming',df['deleteBackground'])]):
        y=65+i*175
        d.rect(16,y,1068,160,background);d.text(28,y+8,title,f['text'],'bold')
        for j,line in enumerate(review_day.CODE[2:5]):
            xx=28
            for role,txt in line:
                d.text(xx,y+39+j*25,txt,{**f,**a}[role],'bold' if role=='clay' else 'regular');xx+=9*len(txt)
        d.text(28,y+126,'Number contrast: '+str(round(wcag(a['ochre'],background),2))+':1',f['text'])
    d.text(24,617,'Codex source preserves syntax foregrounds over the line fill; deletion adds DIM.',f['text'])
    d.text(24,651,'Controlled token specimen, not a native Codex screenshot. Dimming is not simulated.',f['text'])
    d.save('diff-overlay',1100,700,args.png)
    # Adversarial states: make erased text and missing hierarchy visible as evidence.
    for mode in MODES:
        c=lambda value: value if mode=='normal' else simulated_hex(value,mode)
        d=review_day.Drawing();d.rect(0,0,1100,900,c(b['base']))
        d.text(24,18,'Loden Day / stress specimen / '+mode,c(f['text']),'bold')
        d.text(24,55,'Black comments and line numbers share the strongest foreground.',c(f['text']))
        for i in range(6):
            y=88+i*25
            if i==3:d.rect(12,y,1076,25,c(b['surface1']))
            d.text(24,y+2,str(40+i),c(f['muted']))
            d.text(65,y+2,'// Keep this explanation legible during a long review.',c(f['comment']),'italic')
        d.text(24,260,'Current line 43: same number style; only the subtle row fill changes.',c(f['text']))
        d.text(24,305,'Added digit and whitespace: underline on / underline off',c(f['text']),'bold')
        for i,underline in enumerate([True,False]):
            y=343+i*38;d.rect(24,y,1028,28,c(df['addBackground']))
            d.text(33,y+4,'+ limit = 3;    // inserted space at right',c(df['addForeground']))
            for xx,txt in [(123,'3'),(501,' ')]:
                d.rect(xx,y,9,28,c(df['addEmphasis']));d.text(xx,y+4,txt,c(df['inlineForeground']),'bold')
                if underline:d.rect(xx,y+25,9,1,c(df['inlineForeground']))
        d.text(24,438,'Severity words rescue similar info/hint colors.',c(f['text']))
        d.text(24,471,'INFO: extracted type',c(a['blue']));d.text(510,471,'HINT: extracted type',c(a['aqua']))
        d.text(24,515,'ANSI palette collision: these black rectangles contain invisible text.',c(f['text']),'bold')
        for i,(label,x,y) in enumerate([('37;40 white on black','white','black'),('30;47 black on white','black','white'),('97;40 bright white on black','brightWhite','black')]):
            yy=552+i*42;d.text(24,yy+4,label,c(f['text']))
            d.rect(470,yy,580,30,c(p['ansi'][y]));d.text(480,yy+5,'This text cannot be read: contrast 1:1',c(p['ansi'][x]))
        d.text(24,703,'All neutral text remains black in this committed design.',c(f['text']))
        d.text(24,737,'This is a controlled reproduction of token pairs, not a terminal screenshot.',c(f['text']))
        d.text(24,771,'The ANSI cases follow indexed SGR semantics; host contrast correction may vary.',c(f['text']))
        d.text(24,826,'No production colors were changed for this assessment.',c(f['text']))
        d.save('stress-'+mode,1100,900,args.png)
    print('Wrote measurements, comparison, and five stress specimens to',OUT)


if __name__=='__main__':
    main()
