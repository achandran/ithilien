"""Generate the native Neovim diff preview and its provenance."""
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
from ithilienlib import ROOT
from tintprobe.evaluate_theme import capture
from tintprobe.evaluation_checks import effective_colors

def generate(width,state,filename,variant='dawn'):
    nvim=shutil.which('nvim')
    if not nvim:raise RuntimeError('README capture requires Neovim')
    case={'id':'readme-python','before':str(ROOT/'tests/fixtures/readme/before.py'),'after':str(ROOT/'tests/fixtures/readme/after.py'),'filetype':'python','selection_line':7,'require_syntax':True}
    adapter = dict(id='ithilien-'+variant,
        paths=[ROOT],background='light' if variant=='dawn' else 'dark',
        setup=f"require('ithilien').load('{variant}')",
        after_diff="require('ithilien.diff').refresh()")
    shot=capture(case,width,state,nvim,None,adapter)
    if not shot['syntax_groups']:raise RuntimeError('Missing native Python syntax')
    # Rasterize actual cells, with no invented highlight colors.
    commands=[]
    for c in shot['cells']:
        fg,bg=effective_colors(shot,c);x=c['col']*10;y=c['row']*23
        commands.append({'x':x,'y':y,'w':10,'h':23,'color':f'#{bg:06X}'})
    for c in shot['cells']:
        if not c['text'].strip():continue
        fg,_=effective_colors(shot,c);a=shot['attrs'].get(c['attr'],{})
        commands.append({'x':c['col']*10,'y':c['row']*23,'text':c['text'],'color':f'#{fg:06X}','style':('bold-italic' if a.get('italic') else 'bold') if a.get('bold') else ('italic' if a.get('italic') else 'regular')})
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'drawing.json';p.write_text(json.dumps({'width':width*10,'height':690,'commands':commands,'fontWeight':'Medium' if variant=='dawn' else 'Retina'}))
        subprocess.run(['swift','-module-cache-path',temp,str(ROOT/'scripts/render_readme.swift'),str(p),str(ROOT/('docs/assets/'+filename+'.png'))],check=True)
    meta={'fixture_sha256':{name:hashlib.sha256((ROOT/f'tests/fixtures/readme/{name}.py').read_bytes()).hexdigest() for name in ('before','after')},'palette_sha256':hashlib.sha256((ROOT/'palette.json').read_bytes()).hexdigest(),'nvim':subprocess.check_output([nvim,'--version'],text=True).splitlines()[0],'theme_source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'lua/ithilien').rglob('*.lua'))},'kind':f'Native Neovim UI cells rasterized using Berkeley Mono {"Medium" if variant=="dawn" else "Retina"} 16pt; not a terminal screenshot'}
    (ROOT/('docs/assets/'+filename+'.json')).write_text(json.dumps(meta,indent=2)+'\n')


def main():
    generate(140,'diff','ithilien-dawn-neovim')
    generate(140,'diff','ithilien-dusk-neovim','dusk')

if __name__=='__main__':main()
