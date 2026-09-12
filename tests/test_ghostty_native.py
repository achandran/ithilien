import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from capture_ghostty import pixel_gate
from evaluate_ghostty import prepare


def test_blank_or_wrong_capture_fails_calibration():
    colors = ['#8B3037', '#315F46']
    assert not pixel_gate({'counts':{}}, colors)['pass']
    assert not pixel_gate({'counts':{'#8B3037':500}}, colors)['pass']
    assert pixel_gate({'counts':dict.fromkeys(colors, 500)}, colors)['pass']


def test_real_command_fixtures_are_not_native_validation(tmp_path):
    result = prepare(tmp_path)
    assert result['status'] == 'blocked'
    assert not result['pass']
    assert result['coverage']['cursor'] == 'untested'
    rows = {r['id']:r for r in result['results']}
    assert rows['pytest']['exit_code'] == 1  # Intentional failure, not fixture failure.
    assert rows['pytest']['status'] == 'prepared'
    import re
    plain = re.sub(rb'\x1b\[[0-9;]*m', b'', (tmp_path/'pytest.ansi').read_bytes())
    assert b'1 failed, 1 passed' in plain
    assert rows['git-word-diff']['contains_ansi']
    assert b'worker.py' in (tmp_path/'git-diff.ansi').read_bytes()
    assert json.loads((tmp_path/'report.json').read_text())['pass'] is False


def test_capture_failure_remains_blocked(tmp_path, monkeypatch):
    import capture_ghostty
    def denied(*args):
        raise RuntimeError('Screen Recording permission is unavailable')
    monkeypatch.setattr(capture_ghostty, 'capture', denied)
    result = prepare(tmp_path, native_capture=True)
    assert result['status'] == 'blocked'
    assert not result['pass']
    assert 'Screen Recording' in result['reason']
