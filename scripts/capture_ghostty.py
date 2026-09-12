"""Native macOS Ghostty capture worker. Run only where native UI access is allowed."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from uuid import uuid4

from ithilienlib import ROOT, load_palette


def pixel_gate(measurement, colors):
    missing = [color for color in colors if measurement.get('counts', {}).get(color, 0) < 100]
    return {'pass':not missing, 'missing_swatches':missing,
            'scope':'Calibration swatch presence only; does not certify glyph legibility, font, cursor, selection, or content completeness.'}


def emit_scene(payload, ready, release):
    calibration = ''.join(f'\x1b[48;5;{i}m      ' for i in range(1, 7))+'\x1b[0m\n\n'
    os.write(1, ('\x1b[2J\x1b[H'+calibration).encode()+payload.read_bytes()+b'\x1b[0m\n')
    ready.write_text('ready')
    deadline = time.monotonic()+45
    while not release.exists() and time.monotonic() < deadline:
        time.sleep(.1)


def capture(output, report):
    if sys.platform != 'darwin':
        raise RuntimeError('Native Ghostty capture currently requires macOS')
    helper = output/'ghostty-capture'
    subprocess.run(['swiftc', '-module-cache-path', str(output/'swift-cache'),
                    str(ROOT/'scripts/ghostty_capture.swift'), '-o', str(helper)], check=True, timeout=120)
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
        try:
            subprocess.run(['open', '-na', 'Ghostty', '--args', '--config-default-files=false',
                            '--config-file='+str(config), '-e', sys.executable, str(Path(__file__).resolve()),
                            '--emit', str(output/row['ansi']), '--ready', str(ready), '--release', str(release)],
                           check=True, timeout=15)
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
                raise RuntimeError('Fixture window/ready marker not found')
            time.sleep(.5)
            image = output/(row['id']+'.png')
            subprocess.run(['/usr/sbin/screencapture', '-x', '-o', '-l', str(window), str(image)], check=True, timeout=15)
            measurement = json.loads(subprocess.check_output([str(helper), 'pixels', str(image), *colors], timeout=30))
            results.append({'id':row['id'], 'image':image.name, 'pixels':measurement,
                            'calibration':pixel_gate(measurement, colors)})
        finally:
            release.write_text('release')  # Only this fixture child exits; never quits the user's Ghostty.
    report['native_captures'] = results
    report['coverage']['native_pixels'] = 'captured; calibration only'
    report['status'] = 'fail' if any(not r.get('calibration', {}).get('pass') for r in results) else 'incomplete'
    report['reason'] = 'Native command screenshots captured; content, cursor, selection, and readability gates are still unimplemented.'
    report['pass'] = False
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emit', type=Path)
    p.add_argument('--ready', type=Path)
    p.add_argument('--release', type=Path)
    args = p.parse_args()
    if args.emit and args.ready and args.release:
        emit_scene(args.emit, args.ready, args.release)
    else:
        p.error('Use evaluate_ghostty.py --capture to run the capture worker')
