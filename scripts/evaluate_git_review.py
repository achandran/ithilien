"""Pinned native Git plugin screens; no personal Neovim configuration is loaded."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from ithilienlib import ROOT
from evaluate_interactions import isolated_capture, assess
from evaluate_installed_workflows import write_gallery
from evaluation_checks import effective_colors

SCENES=('diffview','diffview-conflict','diffview-search','diffview-visual','neogit','neogit-hunks','gitsigns-preview')

def check(shot,colors):
    errors=[]
    text=shot['text'];windows=shot['evidence']['windows']
    case=shot['case']
    if case.startswith('neogit'):
        for token in ('review.py','pending.py','Staged'):
            if token not in text:errors.append('Missing status content: '+token)
        if not any(w['filetype']=='NeogitStatus' for w in windows):errors.append('Missing Neogit status window')
        if case=='neogit-hunks':
            for token in ('LIMIT = 10','LIMIT = 11'):
                if token not in text:errors.append('Expanded patch absent: '+token)
    elif case=='diffview-conflict':
        if sum(w['diff'] for w in windows)<3:errors.append('Missing three-way conflict panes')
        for token in ('LIMIT = 11','LIMIT = 20','<<<<<<<','>>>>>>>'):
            if token not in text:errors.append('Missing conflict content: '+token)
    else:
        for token in ('LIMIT = 10','LIMIT = 11'):
            if token not in text:errors.append('Missing patch content: '+token)
        if case=='diffview' and sum(w['diff'] for w in windows)<2:errors.append('Missing diff panes')
        if case=='gitsigns-preview' and not any(w['floating'] for w in windows):errors.append('Missing hunk float')
    if case in ('diffview','gitsigns-preview','neogit-hunks'):
        emphasis=int(colors['Celandine'][1:],16)
        rows={}
        for c in shot['cells']:rows.setdefault(c['row'],[]).append(c)
        for fragment in ('LIMIT = 10','LIMIT = 11'):
            found=False
            for row in rows.values():
                row=sorted(row,key=lambda c:c['col'])
                line=''.join(c['text'] for c in row)
                index=line.find(fragment)
                if index>=0:
                    found=True
                    if effective_colors(shot,row[index+len(fragment)-1])[1]!=emphasis:
                        errors.append('Missing inline digit emphasis: '+fragment)
            if not found:errors.append('Missing inline fixture: '+fragment)
    if case=='diffview-visual':
        if shot['evidence'].get('mode')!='V':errors.append('Linewise Visual mode absent')
        if shot['evidence'].get('cursor',[0])[0]!=2:errors.append('Visual fixture cursor must be on the following blank line')
        if shot['evidence'].get('visual',[0,0])[1]!=1:errors.append('Visual fixture anchor must be on the changed line')
    if case in ('diffview-search','diffview-visual'):
        expected=int(colors['Heather' if case=='diffview-search' else 'Briar'][1:],16)
        rows={}
        for c in shot['cells']:rows.setdefault(c['row'],[]).append(c)
        found=False
        for row in rows.values():
            row=sorted(row,key=lambda c:c['col']);line=''.join(c['text'] for c in row)
            start=line.find('LIMIT = 11')
            if start>=0:
                found=True
                targets=row[start+8:start+10] if case=='diffview-search' else row[start:start+10]
                if any(effective_colors(shot,c)[1]!=expected for c in targets):errors.append('Overlap not visible across intended text: '+case)
        if not found:errors.append('Missing overlap target')
    if 'Error' in shot['evidence'].get('messages',''):errors.append('Runtime error in messages')
    allowed={int(v[1:],16) for v in colors.values()}
    off=[c for c in shot['cells'] if effective_colors(shot,c)[1] not in allowed or (c['text'].strip() and effective_colors(shot,c)[0] not in allowed)]
    contrast=assess(shot)
    passed=not errors and not off and not contrast['failures']
    return dict(pass_=passed,failures=errors,off_palette=off,contrast=contrast)

def prepare(fetch=False):
    deps=json.loads((ROOT/'evaluation/git-review-dependencies.json').read_text())
    for d in deps.values():
        path=ROOT/d['path']
        if fetch and not path.exists():
            subprocess.run(['git','clone','--no-checkout',d['url'],str(path)],check=True)
            subprocess.run(['git','-C',str(path),'checkout','--detach',d['revision']],check=True)
    return deps


def run(output,widths=(100,160)):
    output.mkdir(parents=True,exist_ok=True)
    deps=prepare()
    paths=[d['path'] for d in deps.values()]
    adapter={'id':'ithilien-dawn','paths':[str(ROOT),*paths], 'pins':{d['path']:d['revision'] for d in deps.values()},'setup':"""
vim.o.loadplugins=true
vim.cmd('runtime plugin/diffview.lua')
require('diffview').setup({use_icons=false})
require('neogit').setup({disable_hint=true,integrations={diffview=false},disable_signs=true})
require('gitsigns').setup({watch_gitdir={enable=false}})
vim.cmd('colorscheme ithilien-dawn')
"""}
    palette=(ROOT/'palette/ithilien-dawn.json').read_bytes()
    colors=json.loads(palette)['colors'];results=[];shots=[]
    for scene in SCENES:
        for width in widths:
            for state in ('initial','reload'):
                print(scene,width,state,flush=True)
                try:
                    shot=isolated_capture(adapter,width,scene,nvim=shutil.which('nvim'),action=state,workflow=str(ROOT/'evaluation/git-review.lua'))
                    shots.append(shot);r=check(shot,colors);r['pass']=r.pop('pass_')
                except Exception as exc:r={'pass':False,'error':str(exc)}
                results.append(dict(scene=scene,width=width,state=state,**r))
    report={'title':'Git review workflows','pass':all(r['pass'] for r in results),'results':results,'dependencies':deps,'nvim':subprocess.check_output(['nvim','--version'],text=True).splitlines()[0],'render_profile':json.loads((ROOT/'evaluation/render-profile.json').read_text()),'palette_sha256':hashlib.sha256(palette).hexdigest(),'fixture_sha256':hashlib.sha256((ROOT/'evaluation/git-review.lua').read_bytes()).hexdigest(),'scope':'Pinned native Diffview, Neogit status and Gitsigns preview. Isolated Git repository; Neovim RGB cells, not Ghostty pixels or comfort proof.'}
    (output/'report.json').write_text(json.dumps(report,indent=2));(output/'cells.json').write_text(json.dumps(shots))
    write_gallery(output,report,shots)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'evaluation/results/git-review')
    p.add_argument('--fetch-dependencies',action='store_true',help='Fetch missing pinned test plugins')
    args=p.parse_args();prepare(args.fetch_dependencies);raise SystemExit(0 if run(args.output)['pass'] else 1)
