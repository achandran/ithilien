"""Native macOS Ghostty capture worker. Run only where native UI access is allowed."""
import argparse
import json
import os
import shlex
from pathlib import Path
import subprocess
import sys
import time
from uuid import uuid4



def pixel_gate(measurement, colors):
    missing = [color for color in colors if measurement.get('counts', {}).get(color, 0) < 100]
    return {'pass':not missing, 'missing_swatches':missing,
            'scope':'Calibration swatch presence only; does not certify glyph legibility, font, cursor, selection, or content completeness.'}


def emit_scene(payload, ready, release, cursor=None, style="steady-block", control=None):
    calibration = ''.join(f'\x1b[48;5;{i}m      ' for i in range(1, 7))+'\x1b[0m\n\n'
    os.write(1, ('\x1b[2J\x1b[H'+calibration).encode()+payload.read_bytes()+b'\x1b[0m\n')
    def set_cursor(style):
        row,column=cursor
        codes={'blinking-block':1,'steady-block':2,'blinking-underline':3,'steady-underline':4,'blinking-bar':5,'steady-bar':6,'hidden':2}
        visible='l' if style=='hidden' else 'h'
        os.write(1,f'\x1b[{codes[style]} q\x1b[?25{visible}\x1b[{row+3};{column+1}H'.encode())
    if cursor is not None:set_cursor(style)
    ready.write_text('ready')
    deadline = time.monotonic()+45
    sequence=None
    while not release.exists() and time.monotonic() < deadline:
        if control and control.exists():
            request=json.loads(control.read_text())
            if request['sequence']!=sequence:
                set_cursor(request['style']);sequence=request['sequence']
                ready.write_text(str(sequence))
        time.sleep(.05)


def write_launcher(output, name, payload, ready, release, cursor=None, control=None):
    """Keep argument quoting and child errors independent of app launch parsing."""
    launcher = output/(name+'.launch.sh')
    started, log = output/(name+'.started'), output/(name+'.child.log')
    for path in (started, log):
        path.unlink(missing_ok=True)
    command = [sys.executable, str(Path(__file__).resolve()), '--emit', str(payload),
               '--ready', str(ready), '--release', str(release)]
    if cursor is not None:
        command += ['--cursor-row',str(cursor['row']),'--cursor-column',str(cursor['column']), '--cursor-style',cursor.get('style','steady-block')]
    if control:command += ['--control',str(control)]
    launcher.write_text('#!/bin/sh\n'+
        'printf started > '+shlex.quote(str(started))+'\n'+
        'exec '+shlex.join(command)+' 2>'+shlex.quote(str(log))+'\n')
    return launcher, started, log


def timeout_reason(ready, started, log):
    if ready.exists():
        return 'Fixture rendered, but no uniquely titled Ghostty window was found'
    detail = log.read_text(errors='replace').strip() if log.exists() else ''
    if detail:
        return 'Fixture child failed: '+detail[-4000:]
    if started.exists():
        return 'Fixture launcher started, but child did not write the ready marker; inspect '+str(log)
    return 'Ghostty did not start the fixture launcher; inspect its startup/configuration error window'


def build_helper(output):
    from ithilienlib import ROOT
    helper = output/'ghostty-capture'
    subprocess.run(['swiftc', '-module-cache-path', str(output/'swift-cache'),
                    str(ROOT/'scripts/ghostty_capture.swift'), '-o', str(helper)], check=True, timeout=120)
    return helper


def capture(output, report):
    from ithilienlib import ROOT, load_palette
    if sys.platform != 'darwin':
        raise RuntimeError('Native Ghostty capture currently requires macOS')
    helper = build_helper(output)
    # Read-only preflight before launching any fixture windows. Never requests permission.
    subprocess.run([str(helper), 'windows', 'ithilien-preflight'], check=True, capture_output=True, timeout=10)
    palette = load_palette('ithilien-dawn')
    colors = list(dict.fromkeys(list(palette['ansi'].values())[1:7]))
    results = []
    report['native_captures'] = results
    for row in report['results']:
        if row['status'] != 'prepared':
            results.append({'id':row['id'], 'pass':False, 'reason':'Command fixture failed to prepare'})
            continue
        title = 'Ithilien evaluation '+uuid4().hex
        ready, release = output/(title+'.ready'), output/(title+'.release')
        config = output/(row['id']+'.conf')
        config.write_text((output/'ghostty.conf').read_text()+
                          f'\ntitle = {title}\nwindow-width = 120\nwindow-height = 40\n')
        control=output/(row['id']+'.control.json') if row.get('transitions') else None
        if control:control.unlink(missing_ok=True)
        launcher, started, log = write_launcher(output, row['id'], output/row['ansi'], ready, release, row.get('cursor') or ({'row':0,'column':0,'style':'hidden'} if row.get('selection') else None),control)
        launch_command = 'shell:'+shlex.join(['/bin/sh', str(launcher)])
        try:
            subprocess.run(['open', '-na', 'Ghostty', '--args', '--config-default-files=false',
                            '--config-file='+str(config), '--shell-integration=none',
                            '--quit-after-last-window-closed=true', '--initial-command='+launch_command],
                           check=True, timeout=15, capture_output=True)
            deadline = time.monotonic()+20
            window = None
            while time.monotonic() < deadline:
                if ready.exists():
                    found = json.loads(subprocess.check_output([str(helper), 'windows', title], timeout=10))['windows']
                    if len(found) > 1:
                        raise RuntimeError('Ambiguous fixture window; refusing to capture')
                    if found:
                        window = found[0]
                        break
                time.sleep(.2)
            if window is None:
                raise RuntimeError(timeout_reason(ready, started, log))
            if row.get('cursor') or row.get('selection'):
                subprocess.run([str(helper),'focus',title,str(window)],check=True,capture_output=True,timeout=10)
            time.sleep(.5)
            image = output/(row['id']+'.png')
            def grab(path):
                subprocess.run(['/usr/sbin/screencapture','-x','-o','-l',str(window),str(path)],check=True,timeout=15)
            interaction_evidence={}
            if row.get('selection'):
                from ghostty_quality import grid,srgb_image
                from ghostty_interactions import drag_points
                before=output/(row['id']+'.before.png');grab(before)
                decoded=srgb_image(before)
                points=drag_points(grid(decoded,colors),decoded.size,row['selection'])
                subprocess.run([str(helper),'drag',title,str(window),*[str(v) for v in points]],
                               check=True,capture_output=True,timeout=10)
                interaction_evidence={'before_image':before.name,'drag_fractions':points,'input':'native mouse drag','window':window}
                time.sleep(.2)
            frames=[]
            if row.get('transitions'):
                for i,style in enumerate(row['transitions']):
                    pending=control.with_suffix('.pending')
                    pending.write_text(json.dumps({'sequence':i,'style':style}));pending.replace(control)
                    deadline=time.monotonic()+3
                    while ready.read_text()!=str(i):
                        if time.monotonic()>deadline:raise RuntimeError('Cursor transition handshake timed out')
                        time.sleep(.05)
                    time.sleep(.15)
                    path=output/(row['id']+f'.state-{i:02}.png');grab(path)
                    frames.append({'image':path.name,'style':style,'time':time.monotonic()})
                image.write_bytes((output/frames[0]['image']).read_bytes())
            elif row.get('cursor',{}).get('style','').startswith('blinking-'):
                for i in range(16):
                    path=output/(row['id']+f'.phase-{i:02}.png')
                    grab(path);frames.append({'image':path.name,'time':time.monotonic()})
                    time.sleep(.15)
                image.write_bytes((output/frames[0]['image']).read_bytes())
            else:grab(image)
            measurement = json.loads(subprocess.check_output([str(helper), 'pixels', str(image), *colors], timeout=30))
            results.append({'id':row['id'], 'image':image.name, 'pixels':measurement,
                            'frames':frames,'interaction':interaction_evidence,'calibration':pixel_gate(measurement, colors)})
            report['coverage']['native_pixels']=f'{len(results)} framesets captured; per-case quality analysis follows'
            report['render_profile']['light']['native_capture']='captured in Ghostty'
            report['scope']='Native frames captured for the completed cases; missing cases and full native workflows remain unverified.'
        finally:
            release.write_text('release')  # Only this fixture child exits; never quits the user's Ghostty.
    report['native_captures'] = results
    report['coverage']['native_pixels'] = 'captured; per-case quality analysis follows'
    report['render_profile']['light']['native_capture'] = 'captured in Ghostty'
    report['scope'] = ('Native Ghostty screenshots of prepared command output and a labeled ANSI probe. '
                       'Per-case text and interaction gates follow capture; font identity, native editor/agent workflows, and comfort remain unverified.')
    report['status'] = 'fail' if any(not r.get('calibration', {}).get('pass') for r in results) else 'incomplete'
    report['reason'] = 'Native screenshots captured; see per-case command and interaction quality evidence.'
    report['pass'] = False
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emit', type=Path)
    p.add_argument('--ready', type=Path)
    p.add_argument('--release', type=Path)
    p.add_argument('--control', type=Path)
    p.add_argument('--cursor-row', type=int)
    p.add_argument('--cursor-column', type=int)
    p.add_argument('--cursor-style', choices=('steady-block','steady-bar','steady-underline','blinking-block','blinking-bar','blinking-underline','hidden'),default='steady-block')
    args = p.parse_args()
    if args.emit and args.ready and args.release:
        cursor=None
        if args.cursor_row is not None or args.cursor_column is not None:
            if args.cursor_row is None or args.cursor_column is None or not 0<=args.cursor_row<36 or not 0<=args.cursor_column<120:
                p.error('Cursor requires row 0..35 and column 0..119')
            cursor=(args.cursor_row,args.cursor_column)
        emit_scene(args.emit, args.ready, args.release, cursor, args.cursor_style, args.control)
    else:
        p.error('Use evaluate_ghostty.py --capture to run the capture worker')
