"""One command for supported theme comparisons and native Codex evaluations."""
import argparse,json,subprocess,sys,html
from pathlib import Path
import shutil
from ithilienlib import ROOT
from codex_theme_adapters import prepare
from codex_native import run_native
from codex_flows import run as run_flows
from agent_gates import assess
from aesthetic_score import evaluate as evaluate_aesthetic


def execution_failed(report):
    return (any(s['status']!='pass' for s in report['stages'].values())
            or any(t.get('status')=='unavailable_or_error' or not t.get('codex_diff',{}).get('captures') for t in report['themes']))


def write_index(out,report):
    rows=[];details=[]
    for t in report['themes']:
        name=html.escape(t['id'])
        aesthetic=t.get('aesthetic',{'status':'not evaluated','score':None})
        details.append('<details><summary>'+name+': Formex fidelity '+html.escape(str(aesthetic.get('score')) if aesthetic.get('score') is not None else aesthetic['status'])+'</summary><pre>'+html.escape(json.dumps(aesthetic,indent=2))+'</pre></details>')
        if 'adapter' not in t:rows.append(f'<tr><td>{name}</td><td colspan="3">{html.escape(t["reason"])}</td></tr>');continue
        rows.append(f'<tr><td>{name}</td><td>{html.escape(t["adapter"]["provenance"])}</td><td><a href="{t["diff_gallery"]}">{t["codex_diff"]["status"]}: diffs</a></td><td><a href="{t["flow_gallery"]}">{t["agent_gates"]["status"]}: flows</a></td></tr>')
        stage_rows=''.join(f'<tr><td>{html.escape(g["stage"])}</td><td>{g["width"]}</td><td>{g["minimum_contrast"]}</td><td>{len(g["failures"])}</td><td>{g["dim_cells_unverified"]}</td></tr>' for g in t['agent_gates']['stages'])
        details.append(f'<details><summary>{name}: agent-stage measurements</summary><p>Whole frame including accumulated history. Required-content fragment findings are in <a href="codex/{t["id"]}/agent-gates.json">agent-gates.json</a>.</p><table><tr><th>Stage</th><th>Width</th><th>Minimum contrast</th><th>Failed cells</th><th>Dim cells (unverified)</th></tr>{stage_rows}</table></details>')

    (out/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Theme suite</title><style>body{font:16px/1.5 system-ui;padding:30px}td,th{padding:12px;border-bottom:1px solid #ccc}</style><h1>Combined evaluation</h1><p>Supported stages completed separately from quality gates. Full coverage remains incomplete: Ghostty, Claude Code, and comfort are unverified. Native event replay, not live model sessions.</p><p><a href="neovim/scorecard.html">Neovim gates</a> · <a href="python/scorecard.html">Python Tree-sitter/LSP gates</a> · <a href="interactions/gallery.html">fzf / diagnostics / completion</a> · <a href="report.json">Full evidence</a></p><table><tr><th>Theme</th><th>Codex adapter provenance</th><th>Diff gates</th><th>Flow gates</th></tr>'+''.join(rows)+'</table><p>Converted ports test our explicit mapping, not an upstream author’s Codex implementation.</p>'+''.join(details))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--codex-source',type=Path,required=True);p.add_argument('--python-source',type=Path,required=True)
    p.add_argument('--manifest',type=Path,default=ROOT/'evaluation/themes.json');p.add_argument('--output',type=Path,default=ROOT/'evaluation/results/suite')
    p.add_argument('--skip-fzf',action='store_true');p.add_argument('--themes',nargs='+');p.add_argument('--strict-gates',action='store_true');p.add_argument('--nvim',default=shutil.which('nvim'))
    a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    entries=json.loads(a.manifest.read_text())
    if a.themes:
        if set(a.themes)-{x['id'] for x in entries}:p.error('Unknown theme')
        entries=[x for x in entries if x['id'] in a.themes]
    report={'stages':{},'themes':[],'coverage':{'ghostty':'blocked by Computer Use policy','claude_code':'not evaluated','long_session_comfort':'not evaluated','full_target_coverage':'incomplete'}}
    for name,extra in [('neovim',[]),('python',['--python-source',str(a.python_source.resolve())])]:
        print('Stage: '+name,flush=True)
        cmd=[sys.executable,str(ROOT/'scripts/compare_themes.py'),'--manifest',str(a.manifest.resolve()),'--output',str(out/name),'--nvim',a.nvim,'--themes',*[e['id'] for e in entries],*extra]
        result=subprocess.run(cmd,cwd=ROOT)
        report['stages'][name]={'status':'pass' if result.returncode==0 else 'fail','gallery':name+'/gallery.html','scorecard':name+'/scorecard.html'}
    for entry in entries:
        name=entry['id'];print('Codex: '+name,flush=True);folder=out/'codex'/name
        try:
            theme,palette,meta=prepare(entry,folder/'adapter',a.nvim)
            diff=run_native(a.codex_source.resolve(),folder/'diff',theme,palette)
            flow=run_flows(a.codex_source.resolve(),folder/'flows',theme,palette)
            records=json.loads((folder/'flows/codex-cells.json').read_text());gates=assess(records,palette)
            (folder/'agent-gates.json').write_text(json.dumps(gates,indent=2))
            report['themes'].append({'id':name,'aesthetic':evaluate_aesthetic(entry,palette,records),'adapter':meta,'codex_diff':diff,'codex_flows':flow,'agent_gates':gates,'flow_gallery':f'codex/{name}/flows/codex-gallery.html','diff_gallery':f'codex/{name}/diff/codex-gallery.html'})
        except Exception as exc:
            report['themes'].append({'id':name,'status':'unavailable_or_error','reason':str(exc)})
        (out/'report.json').write_text(json.dumps(report,indent=2))
    from evaluate_interactions import run as run_interactions
    interactions=run_interactions(entries,out/'interactions',a.nvim,include_fzf=not a.skip_fzf)
    report['interactions']={'gallery':'interactions/gallery.html','report':'interactions/report.json','quality_pass':all(r['quality_pass'] for r in interactions['results'])}
    report['stages']['interactions']={'status':'fail' if any(r['errors'] for r in interactions['results']) else 'pass'}
    failures=execution_failed(report)
    if a.strict_gates:
        failures |= not report['interactions']['quality_pass']
        for stage in ('neovim','python'):
            path=out/stage/'scorecard.json'
            if not path.exists():failures=True;continue
            failures |= any(t['gates']['failures'] for t in json.loads(path.read_text())['results'])
        failures |= any(t.get('codex_diff',{}).get('status')!='pass' or t.get('agent_gates',{}).get('status')!='pass' for t in report['themes'])
    report['required_execution_status']='fail' if failures else 'complete';report['strict_gates']=a.strict_gates
    (out/'report.json').write_text(json.dumps(report,indent=2))
    write_index(out,report)
    return int(failures)

if __name__=='__main__':raise SystemExit(main())
