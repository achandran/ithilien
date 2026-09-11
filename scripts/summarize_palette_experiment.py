"""Summarize a completed bounded experiment without claiming a composite winner."""
import json,html,sys
from pathlib import Path
from evaluate_suite import write_index
out=Path(sys.argv[1]);screen=json.loads((out/'screening.json').read_text());rows=[];summary=[]
for candidate in screen['candidates']:
    name=candidate['id'];folder=out/name
    if not (folder/'report.json').exists():continue
    report=json.loads((folder/'report.json').read_text());theme=report['themes'][0]
    measurements={stage:json.loads((folder/stage/'scorecard.json').read_text())['results'][0]['gates'] for stage in ('neovim','python')}
    record={'id':name,'changes':candidate['changes'],'execution':report['required_execution_status'],'gates':measurements,'codex_diff':theme.get('codex_diff',{}).get('status'),'codex_flows':theme.get('agent_gates',{}).get('status'),'screen_metrics':candidate['metrics']};summary.append(record)
    g=measurements['neovim'];dist=g['distributions']
    cells=[name,str(candidate['changes']),str(dist['text_contrast']['minimum']),str(dist['line_delta_e']['minimum']),str(dist['inline_delta_e']['minimum']),str(len(g['failures'])),str(len(measurements['python']['failures'])),str(record['codex_diff'])+'/'+str(record['codex_flows'])]
    rows.append('<tr>'+''.join('<td>'+html.escape(c)+'</td>' for c in cells)+f'<td><a href="{name}/index.html">Native evidence</a></td></tr>')
    write_index(folder,report)
(out/'comparison.json').write_text(json.dumps(summary,indent=2))
(out/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Palette experiment</title><style>body{font:16px/1.5 system-ui;margin:32px}td,th{padding:10px;border-bottom:1px solid #ccc}table{border-collapse:collapse}</style><h1>Ithilien Dawn: bounded palette experiment</h1><p>12 candidates screened; baseline plus three native evaluations. No installed theme changes. Font request: Berkeley Mono Medium, 16pt.</p><p>Compare uncapped measurements; higher separation is not proof of better comfort. Legacy composite scores saturate. Formex score is unchanged because these edits affect functional diff colors, not ordinary request-frame identity.</p><table><tr><th>Candidate</th><th>Changes</th><th>Minimum text contrast</th><th>Line ΔE</th><th>Inline ΔE</th><th>Neovim failures</th><th>Python failures</th><th>Codex diff/flows</th><th>Evidence</th></tr>'''+''.join(rows)+'''</table><p>Recommendation: examine candidate-04 first: it changes only the line background. Candidate-06 adds deeper amber; candidate-10 increases line contrast further. Keep baseline if the stronger fills feel intrusive. Readability gates are safeguards, not evidence of faster review or long-session comfort.</p><p>Ghostty native pixels, Claude Code and sustained comfort remain unverified. The baseline Python stage was rerun successfully after fixing the isolated virtual-environment path.</p><a href="comparison.json">Measurements</a> · <a href="screening.json">All screened variations</a>''')
