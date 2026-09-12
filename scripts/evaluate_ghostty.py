"""Prepare real terminal-command evidence; require native captures for acceptance."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from ithilienlib import ROOT


def prepare(output, native_capture=False):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    records = []
    env = dict(os.environ, TERM='xterm-256color', COLORTERM='truecolor',
               FORCE_COLOR='1', CLICOLOR_FORCE='1', LC_ALL='C', TZ='UTC',
               GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTEST_ADDOPTS='')
    env.pop('NO_COLOR', None)
    with tempfile.TemporaryDirectory(prefix='ithilien-terminal-') as tmp:
        cwd = Path(tmp)
        before = 'def retry(attempt):\n    return attempt < 3\n'
        after = 'def retry(attempt):\n    return attempt <= 3\n'
        (cwd/'worker.py').write_text(before)
        git = shutil.which('git')
        if not git:
            raise FileNotFoundError('git is required for terminal command fixtures')
        subprocess.run([git, 'init', '-q', str(cwd)], env=env, check=True)
        subprocess.run([git, '-C', str(cwd), 'add', 'worker.py'], env=env, check=True)
        (cwd/'worker.py').write_text(after)
        (cwd/'test_worker.py').write_text('from worker import retry\n\ndef test_pass():\n    assert retry(2)\n\ndef test_boundary():\n    assert not retry(3)\n')
        commands = [
            ('git-status', [git, '-c', 'color.status=always', 'status', '--short'], 0),
            ('git-diff', [git, '--no-pager', 'diff', '--color=always', '--', 'worker.py'], 0),
            ('git-word-diff', [git, '--no-pager', 'diff', '--color=always', '--word-diff=color', '--word-diff-regex=.', '--', 'worker.py'], 0),
            ('pytest', [sys.executable, '-m', 'pytest', '-q', '--color=yes', '--tb=short', 'test_worker.py'], 1),
        ]
        zsh = shutil.which('zsh')
        if zsh:
            commands.append(('zsh-prompt', [zsh, '-f', '-c', 'source "$1"; vcs_info_msg_0_="(main)"; print -P -- "$PS1"; print -r -- "uv run pytest -q tests/test_worker.py"', 'fixture', str(ROOT/'shell/prompt.zsh')], 0))
        else:
            records.append({'id':'zsh-prompt', 'status':'blocked', 'reason':'zsh executable missing'})
        rg = shutil.which('rg')
        if rg:
            commands.append(('ripgrep', [rg, '--color=always', '--line-number', 'attempt|retry', 'worker.py'], 0))
        else:
            records.append({'id':'ripgrep', 'status':'blocked', 'reason':'rg executable missing'})
        for name, command, expected in commands:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=60)
            path = output/(name+'.ansi')
            path.write_bytes(result.stdout)
            records.append({'id':name, 'status':'prepared' if result.returncode==expected else 'fail',
                'command':command, 'exit_code':result.returncode, 'expected_exit_code':expected,
                'ansi':path.name, 'sha256':hashlib.sha256(result.stdout).hexdigest(),
                'contains_ansi':b'\x1b[' in result.stdout})
    # These are explicit probes, not purported output from a particular application.
    probe = '\x1b[0mNormal: Aa 0O 1lI [] {} != ->\n\x1b[2mDim: deleted token / existing code\x1b[0m\n'
    for index in range(16):
        probe += f'\x1b[38;5;{index}mANSI {index:02}: Aa 0O 1lI [] {{}} != ->\x1b[0m\n'
    (output/'attributes.ansi').write_text(probe)
    records.append({'id':'attributes', 'status':'prepared', 'ansi':'attributes.ansi',
                    'sha256':hashlib.sha256(probe.encode()).hexdigest(), 'contains_ansi':True})
    from ghostty_glyphs import reference_sheet
    atlas, _ = reference_sheet()
    (output/'glyph-reference.ansi').write_text(atlas)
    records.append({'id':'glyph-reference', 'kind':'glyph-reference', 'status':'prepared',
                    'ansi':'glyph-reference.ansi', 'sha256':hashlib.sha256(atlas.encode()).hexdigest(), 'contains_ansi':True})
    cursor_text='return attempt <= 3\n'
    (output/'cursor-block.ansi').write_text(cursor_text)
    records.append({'id':'cursor-block','kind':'cursor','status':'prepared','ansi':'cursor-block.ansi',
                    'sha256':hashlib.sha256(cursor_text.encode()).hexdigest(),'contains_ansi':False,
                    'cursor':{'row':0,'column':cursor_text.index('='),'text':'=','style':'steady-block'}})
    theme = ROOT/'ghostty/themes/ithilien_dawn.conf'
    config = theme.read_text()+'\nfont-size = 16\nwindow-colorspace = srgb\n'
    (output/'ghostty.conf').write_text(config)
    report = {'status':'blocked', 'pass':False, 'results':records,
        'reason':'Native Ghostty capture provider unavailable; prepared command output is not pixel validation.',
        'theme_sha256':hashlib.sha256(theme.read_bytes()).hexdigest(),
        'render_profile':json.loads((ROOT/'evaluation/render-profile.json').read_text()),
        'coverage':{'terminal_commands':'real subprocess output prepared; not visually validated',
                    'ansi_and_dim':'probe prepared; not visually validated',
                    'cursor':'untested', 'selection':'untested', 'neovim':'untested in Ghostty',
                    'codex':'untested in Ghostty', 'native_pixels':'blocked'},
        'scope':'No screenshots taken. ANSI files contain real command bytes except the labeled attribute probe. Pytest intentionally exercises one passing and one failing test. Native UI automation is a required separate dependency.'}
    if native_capture:
        from capture_ghostty import capture
        try:
            report = capture(output, report)
        except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
            detail = getattr(exc, 'stderr', None)
            if isinstance(detail, bytes):
                detail = detail.decode('utf-8', errors='replace')
            report['reason'] = 'Native capture failed: '+(detail.strip() if detail and detail.strip() else str(exc))
    (output/'report.json').write_text(json.dumps(report, indent=2))
    if report.get('native_captures'):
        from ghostty_quality import analyze
        try:
            report['command_quality']=analyze(output, output/'ghostty-capture')
        except (OSError,ValueError,subprocess.SubprocessError) as exc:
            report['command_quality']={'status':'unverified','reason':str(exc)}
        cursor_results=[r.get('cursor',{}) for r in report['command_quality'].get('results',[]) if r['id']=='cursor-block']
        if cursor_results:
            report['coverage']['cursor']='Steady block over equals: '+cursor_results[0].get('status','unverified')+'; other modes untested'
        report['reason']='See command_quality for command and steady-block cursor checks. Mouse selection and other cursor modes remain untested.'
        (output/'report.json').write_text(json.dumps(report, indent=2))
    links=''.join(f'<li>{html.escape(r["id"])}: {html.escape(r["status"])}'+
                  (f' — <a href="{r["ansi"]}">ANSI bytes</a>' if 'ansi' in r else '')+'</li>' for r in records)
    images=''.join('<h2>'+html.escape(r['id'])+'</h2><img style="max-width:100%" src="'+r['image']+'">' for r in report.get('native_captures',[]) if 'image' in r)
    (output/'gallery.html').write_text('<!doctype html><meta charset="utf-8"><h1>Ghostty validation</h1><p>'+html.escape(report['reason'])+'</p><ul>'+links+'</ul>'+images+'<p>ANSI links contain command bytes. Any PNGs above are native captures with calibration and separate text-check evidence, not full readability validation.</p><a href="report.json">Evidence and coverage</a> · <a href="quality.html">Text checks</a>')
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'evaluation/results/ghostty')
    parser.add_argument('--capture', action='store_true', help='Launch and capture isolated native Ghostty windows on an authorized macOS host')
    args=parser.parse_args()
    report=prepare(args.output, args.capture)
    print(json.dumps(report, indent=2))
    sys.exit(1)  # Preparing fixtures cannot satisfy native Ghostty acceptance.
