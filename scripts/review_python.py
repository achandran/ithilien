"""Compare actual Python Tree-sitter captures with bat's Syntect/TextMate output.

Requires KANSO_ROOT, TS_ROOT (nvim-treesitter/runtime), TS_SITE (nvim/site).
Uses isolated bat configuration/cache and never installs a personal theme.
"""
import json
import io
import keyword
import os
import re
import shutil
import subprocess
import tempfile
import tokenize
from pathlib import Path
from unittest.mock import patch
import review_day
from lodenlib import ROOT,load_palette,wcag

OUT=ROOT/'reports/python-review'

def check_roles(rows, palette):
    """Check parsed output, including negative cases for overbroad scope rules."""
    count = 0
    def expect(line, start, text, color, bold=None):
        nonlocal count
        cells = rows[line-1]['cells'][start:start+len(text)]
        assert ''.join(c['text'] for c in cells) == text
        for cell in cells:
            style = cell['style']
            assert style.get('fg', 0) == int(color[1:], 16), (line, text, style, color)
            if bold is not None:
                assert bool(style.get('bold')) == bold, (line, text, style)
                assert not style.get('italic'), (line, text, style)
        count += 1

    source = (OUT/'sample.py').read_text()
    compile(source, 'sample.py', 'exec')
    a = palette['accents']
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        line, col = token.start
        if token.type == tokenize.NAME and keyword.iskeyword(token.string):
            if token.string in {'True', 'False', 'None'}:
                expect(line, col, token.string, a['ochre'])
            elif token.string in {'and', 'or', 'not', 'is', 'in'}:
                expect(line, col, token.string, a['olive'], False)
            else:
                expect(line, col, token.string, a['clay'], True)
    for line, text, role in [
        (10,'RetryPolicy','aqua'), (15,'describe','gold'), (22,'read_names','gold'),
        (22,'Path','aqua'), (27,'Iterable','aqua'), (31,'fetch','gold'),
        (42,'RetryPolicy','gold'), (43,'read_names','gold'), (43,'Path','gold'),
        (9,'dataclass','ochre'), (21,'lru_cache','ochre'), (42,'MAX_RETRIES','ochre'),
        (17,'retry','sage'), (43,'jobs.txt','sage'),
    ]:
        expect(line, rows[line-1]['text'].index(text), text, a[role])
    for line, text in [(17,'label'), (17,'prefix'), (31,'response'), (31,'client'),
                       (31,'name'), (42,'policy'), (43,'names'), (18,'label')]:
        expect(line, rows[line-1]['text'].index(text), text, palette['foregrounds']['text'])
    expect(11, 4, rows[10]['text'][4:], palette['foregrounds']['comment'])
    return count

def ansi_rows(value):
    fg=0;bold=italic=False;rows=[]
    for line in value.splitlines():
        cells=[];pos=0
        for m in re.finditer(r'\x1b\[([0-9;]*)m',line):
            for c in line[pos:m.start()]:cells.append(dict(text=c,style=dict(fg=fg,bold=bold,italic=italic)))
            codes=[int(x or 0) for x in m[1].split(';')];i=0
            while i<len(codes):
                n=codes[i]
                if n==0:fg=0;bold=italic=False
                elif n==1:bold=True
                elif n==3:italic=True
                elif n==22:bold=False
                elif n==23:italic=False
                elif n==39:fg=0
                elif n in (38,48) and codes[i+1]==2:
                    if n==38:fg=(codes[i+2]<<16)+(codes[i+3]<<8)+codes[i+4]
                    i+=4
                else:raise ValueError(f'Unhandled SGR code {codes}')
                i+=1
            pos=m.end()
        for c in line[pos:]:cells.append(dict(text=c,style=dict(fg=fg,bold=bold,italic=italic)))
        rows.append(dict(text=''.join(c['text'] for c in cells),cells=cells))
    return rows

def main():
    env=dict(os.environ,NVIM_LOG_FILE='/private/tmp/loden-python.log')
    subprocess.run(['nvim','--headless','-u','NONE','-i','NONE','-l','scripts/check_python_syntax.lua'],env=env,check=True)
    native=json.loads((OUT/'neovim.json').read_text())
    with tempfile.TemporaryDirectory(prefix='loden-python-',dir='/private/tmp') as t:
        root=Path(t);(root/'config/themes').mkdir(parents=True)
        shutil.copy(ROOT/'codex/themes/loden-day.tmTheme',root/'config/themes/loden-day.tmTheme')
        env=dict(os.environ,COLORTERM='truecolor',BAT_CONFIG_DIR=str(root/'config'),BAT_CACHE_PATH=str(root/'cache'))
        subprocess.run(['bat','cache','--build'],env=env,capture_output=True,check=True)
        r=subprocess.run(['bat','--plain','--color=always','--paging=never','--theme=loden-day',str(OUT/'sample.py')],env=env,capture_output=True,text=True,check=True)
        assert not r.stderr,r.stderr # Unknown theme warnings must not silently fall back.
        (OUT/'textmate.ansi').write_text(r.stdout)
    mate=ansi_rows(r.stdout)
    assert [r['text'] for r in native['rows']]==[r['text'] for r in mate]
    p=load_palette('loden-day');bg=p['backgrounds']['base']
    summary={}
    d=review_day.Drawing();width=1880;height=1120
    d.rect(0,0,width,height,'#D0CEC5')
    for x,rows,label,key in [(0,native['rows'],'Neovim / actual Python Tree-sitter roles','treesitter'),(950,mate,'TextMate / bat Syntect with Loden theme','textmate')]:
        d.rect(x,0,930,height,bg);d.text(x+15,12,label,'#000000','bold')
        d.text(x+15,40,'15 px Berkeley Mono / reconstructed from captured styles',p['foregrounds']['subtext'])
        ratios=[]
        for i,row in enumerate(rows):
            y=76+i*23;d.text(x+12,y,f'{i+1:2}',p['foregrounds']['muted'])
            for col,c in enumerate(row['cells']):
                s=c['style'];fg=f"#{s.get('fg',0):06X}"
                style='bold-italic' if s.get('bold') and s.get('italic') else 'bold' if s.get('bold') else 'italic' if s.get('italic') else 'regular'
                d.text(x+46+col*9,y,c['text'],fg,style)
                if c['text'].strip():ratios.append(wcag(fg,bg))
        checks = check_roles(rows, p)
        assert min(ratios) >= 4.5, (key, min(ratios))
        summary[key]={'minimumTextContrast':min(ratios),'lines':len(rows),'roleChecks':checks}
    subprocess.run(['swiftc','-module-cache-path','/private/tmp/loden-swift-cache',str(ROOT/'scripts/render_review.swift'),'-o','/private/tmp/loden-render-review'],check=True)
    with patch.object(review_day,'OUT',OUT):d.save('comparison',width,height,True)
    native['batVersion']=subprocess.check_output(['bat','--version'],text=True).strip()
    native['kansoCommit']=subprocess.check_output(['git','-C',os.environ['KANSO_ROOT'],'rev-parse','HEAD'],text=True).strip()
    native['treeSitterCommit']=subprocess.check_output(['git','-C',str(Path(os.environ['TS_ROOT']).parent),'rev-parse','HEAD'],text=True).strip()
    native['parserRevision']=(Path(os.environ['TS_SITE'])/'parser-info/python.revision').read_text().strip()
    native['textmateRows']=mate
    (OUT/'neovim.json').write_text(json.dumps(native,separators=(',',':'))+'\n')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))

if __name__=='__main__':main()
