"""Offline corpus + native Neovim UI capture. Missing native Codex is never a pass."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import signal
import pynvim
from ithilienlib import ROOT, load_palette, wcag
from evaluation_checks import state_failures, compare_reports


def capture(case, width, state, nvim_bin, kanso, adapter=None):
    def timed_out(*_): raise TimeoutError('Neovim UI capture timed out')
    signal.signal(signal.SIGALRM, timed_out); signal.alarm(10)
    n = pynvim.attach('child', argv=[nvim_bin, '--embed', '--headless', '-n', '-u', 'NONE', '-i', 'NONE'])
    grid, attrs, defaults = {}, {}, {}
    syntax_groups = []
    highlights = {}
    def notify(name, args):
        if name == 'evaluation_done':
            n.stop_loop(); return
        if name != 'redraw': return
        for event in args:
            for item in event[1:]:
                if event[0] == 'default_colors_set': defaults.update(fg=item[0], bg=item[1])
                elif event[0] == 'hl_attr_define': attrs[item[0]] = item[1]
                elif event[0] == 'grid_clear': grid.clear()
                elif event[0] == 'grid_line':
                    _, row, col, cells, *_ = item
                    attr = 0
                    for cell in cells:
                        if len(cell) > 1: attr = cell[1]
                        for _ in range(cell[2] if len(cell) > 2 else 1):
                            grid[row, col] = (cell[0], attr); col += 1
    def setup():
        nonlocal syntax_groups, highlights
        n.ui_attach(width, 30, rgb=True, ext_linegrid=True)
        n.command('set termguicolors splitright background=light')
        if adapter:
            for path in adapter['paths']: n.exec_lua('vim.opt.rtp:prepend(...)',str(path))
            n.exec_lua(adapter['setup'])
        else:
            n.exec_lua('vim.opt.rtp:prepend(...); vim.opt.rtp:prepend(select(2,...))', str(kanso), str(ROOT))
            n.exec_lua("require('ithilien').load('dawn'); require('ithilien.diff').setup()")
        highlights = n.exec_lua("local out={}; for _,name in ipairs({'Normal','Visual','Search','DiffAdd','DiffDelete','DiffChange','DiffText'}) do out[name]=vim.api.nvim_get_hl(0,{name=name,link=false}) end; return out")
        n.command('filetype on'); n.command('syntax on')
        before = ROOT/'evaluation'/case['before']; after = ROOT/'evaluation'/case['after']
        n.command('edit '+n.funcs.fnameescape(str(before)))
        n.command('setlocal filetype='+case['filetype'])
        n.command('diffthis')
        n.command('vsplit '+n.funcs.fnameescape(str(after)))
        n.command('setlocal filetype='+case['filetype'])
        n.command('diffthis')
        n.command('setlocal nofoldenable')
        n.command('windo setlocal nofoldenable')
        if not adapter: n.exec_lua("require('ithilien.diff').refresh()")
        n.command('normal! gg')
        if state == 'search':
            n.funcs.setreg('/', case.get('search','return\\|font\\|println')); n.command('set hlsearch')
        elif state.startswith('selection'):
            n.command('normal! '+str(case.get('selection_line',2))+'G0')
            keys={'selection':'V2j','selection-char':'v3l','selection-block':'\x163l2j'}[state]
            n.command('normal! '+keys)
        syntax_groups = n.exec_lua("local groups = {}; for row,line in ipairs(vim.api.nvim_buf_get_lines(0,0,-1,false)) do for col=1,#line do local name=vim.fn.synIDattr(vim.fn.synID(row,col,1),'name'); if name ~= '' then groups[name]=true end end end; return vim.tbl_keys(groups)")
        n.command('redraw!')
        n.exec_lua("local ch=...; vim.defer_fn(function() vim.cmd('redraw!'); vim.rpcnotify(ch,'evaluation_done') end,100)",n.channel_id)
    try:
        n.run_loop(None, notify, setup_cb=setup)
        result = {'case':case['id'],'width':width,'state':state,'highlights':highlights,'syntax_groups':syntax_groups,'require_syntax':case.get('require_syntax',False),'defaults':defaults,'attrs':attrs,
                  'cells':[{'row':r,'col':c,'text':t,'attr':a} for (r,c),(t,a) in sorted(grid.items())]}
        assert result['cells'], 'No native UI cells received'
        return result
    finally:
        try: n.command('qa!')
        except (EOFError, OSError): pass
        n.close()
        signal.alarm(0)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kanso', type=Path, required=True)
    parser.add_argument('--nvim', default=shutil.which('nvim'))
    parser.add_argument('--output', type=Path, default=ROOT/'evaluation/results')
    parser.add_argument('--codex-source',type=Path)
    parser.add_argument('--baseline',type=Path,help='Previous results directory for comparison')
    parser.add_argument('--require-codex',action='store_true',help='Fail if native Codex tests cannot run')
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    sources=json.loads((ROOT/'evaluation/sources.json').read_text())
    for entry in [f for source in sources.values() for f in source['files']]:
        assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
    native_checks=[]
    for script in ('check_day_diff.lua','check_diff_presentation.lua'):
        result=subprocess.run([args.nvim,'--headless','-n','-u','NONE','-i','NONE','-l','scripts/'+script],cwd=ROOT,env=dict(os.environ,KANSO_ROOT=str(args.kanso.resolve())),capture_output=True,text=True,timeout=30)
        native_checks.append({'script':script,'passed':result.returncode==0,'output':result.stdout+result.stderr})
    cases=json.loads((ROOT/'evaluation/cases.json').read_text())
    captures=[capture(c,w,s,args.nvim,args.kanso.resolve()) for c in cases for w in (100,160) for s in ('diff','search','selection','selection-char','selection-block')]
    palette=load_palette('ithilien-dawn')
    failures=[{'native_check':c['script'],'error':c['output']} for c in native_checks if not c['passed']]; pairs={}
    for shot in captures:
        failures.extend(state_failures(shot,palette))
        for cell in shot['cells']:
            if not cell['text'].strip(): continue
            attr=shot['attrs'].get(cell['attr'],{})
            fg=attr.get('foreground',shot['defaults']['fg']); bg=attr.get('background',shot['defaults']['bg'])
            if attr.get('reverse'): fg,bg=bg,fg
            ratio=wcag(f'#{fg:06X}',f'#{bg:06X}')
            # Filler dots and structural separators aren't ordinary text.
            threshold=3 if cell['text'] in ('·','│','─','~') else 4.5
            key=f'{fg:06X}/{bg:06X}/{threshold}'
            pairs[key]=round(ratio,3)
            if ratio<threshold: failures.append({'case':shot['case'],'state':shot['state'],'cell':cell,'contrast':ratio})
    native={'status':'not_run','reason':'Native Codex needs a pinned source checkout and Rust; fixtures alone do not validate its renderer.'}
    if args.codex_source:
        from codex_native import run_native
        native=run_native(args.codex_source.resolve(),args.output)
    report={'native_checks':native_checks,'nvim_version':subprocess.check_output([args.nvim,'--version'],text=True).splitlines()[0],'native_neovim_captures':len(captures),'pair_contrasts':pairs,'failures':failures,'codex':native,
            'comfort':'manual assessment required','palette_sha256':hashlib.sha256((ROOT/'palette/ithilien-dawn.json').read_bytes()).hexdigest()}
    if args.baseline:
        old=json.loads((args.baseline/'report.json').read_text())
        (args.output/'comparison.json').write_text(json.dumps(compare_reports(old,report),indent=2)+'\n')
    (args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    (args.output/'cells.json').write_text(json.dumps(captures,ensure_ascii=False)+'\n')
    blocks=[]
    for shot in captures:
        rows={}
        for c in shot['cells']: rows.setdefault(c['row'],[]).append(c)
        lines=[]
        for cells in rows.values():
            spans=[]
            for c in cells:
                a=shot['attrs'].get(c['attr'],{});fg=a.get('foreground',shot['defaults']['fg']);bg=a.get('background',shot['defaults']['bg'])
                if a.get('reverse'):fg,bg=bg,fg
                style=f'color:#{fg:06x};background:#{bg:06x};'+('font-weight:bold;' if a.get('bold') else '')+('font-style:italic;' if a.get('italic') else '')+('text-decoration:underline;' if a.get('underline') else '')
                spans.append(f'<span style="{style}">{html.escape(c["text"])}</span>')
            lines.append(''.join(spans))
        blocks.append(f'<h2>{shot["case"]} · {shot["width"]} columns · {shot["state"]}</h2><pre>'+ '\n'.join(lines)+'</pre>')
    (args.output/'gallery.html').write_text('<!doctype html><meta charset="utf-8"><title>Ithilien native cell gallery</title><style>body{background:#eee;padding:24px}pre{font:14px/1.4 monospace;overflow:auto}h2{font:18px sans-serif}</style><h1>Native Neovim cell captures</h1><p>Browser reconstruction of actual UI cells; not a Ghostty screenshot. Codex validation status is in report.json. Review missed edits, selection visibility and comfort separately.</p>'+''.join(blocks))
    print(json.dumps(report,indent=2))
    return bool(failures) or native['status']=='fail' or (args.require_codex and native['status']!='pass')
if __name__=='__main__':sys.exit(main())
