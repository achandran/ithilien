"""A saved replay must match the explicitly requested variant's export."""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import check_codex_recording as recording


def test_dawn_recording_cannot_certify_dusk(tmp_path):
    cells = tmp_path / 'codex-cells.json'
    cells.write_text('[]')
    dawn = recording.ROOT / 'extras/codex/themes/ithilien-dawn.tmTheme'
    (tmp_path / 'report.json').write_text(json.dumps({
        'status': 'pass', 'theme_sha256': hashlib.sha256(dawn.read_bytes()).hexdigest(),
    }))
    assert recording.check(cells, 'ithilien-dusk')['status'] == 'blocked'


def test_matching_dusk_recording_uses_dusk_palette(tmp_path, monkeypatch):
    cells = tmp_path / 'codex-cells.json'
    cells.write_text('[]')
    theme = recording.ROOT / 'extras/codex/themes/ithilien-dusk.tmTheme'
    (tmp_path / 'report.json').write_text(json.dumps({
        'status': 'pass', 'theme_sha256': hashlib.sha256(theme.read_bytes()).hexdigest(),
    }))
    def assess(cells, palette):
        assert palette['slug'] == 'ithilien-dusk'
        return {'status': 'pass'}
    monkeypatch.setattr(recording, 'assess', assess)
    assert recording.check(cells, 'ithilien-dusk')['status'] == 'pass'
