import sys
import tomllib
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from codex_config import configure
from install import Installer


@pytest.mark.parametrize('text', [
    '', '[tui]\nanimations = true # keep this comment\ntheme = "ithilien-dawn"\n',
    'tui.animations = true\n[projects."/work"]\ntrust_level = "trusted"\n',
    '["tui"]\n"animations" = true\n', '[tui]',
    'tui.theme = "ithilien-dawn"\n',
    'model = "unchanged"\n[tui]\nnotifications = true\n[other]\nanimations = true\n',
])
def test_motion_edit_preserves_other_settings_and_is_idempotent(text):
    expected = tomllib.loads(text)
    expected.setdefault('tui', {})['animations'] = False
    result = configure(text)
    assert tomllib.loads(result) == expected
    assert configure(result) == result
    if '# keep this comment' in text:
        assert '# keep this comment' in result


def test_unhandled_inline_table_is_not_rewritten():
    with pytest.raises(ValueError):
        configure('tui = {animations = true, theme = "keep"}\n')


def test_codex_install_backs_up_config_and_dry_run_does_not_write(tmp_path, monkeypatch):
    base = tmp_path / 'custom-codex'
    base.mkdir()
    monkeypatch.setenv('CODEX_HOME', str(base))
    config = base / 'config.toml'
    original = '[tui]\nanimations = true\ntheme = "ithilien-dawn"\n'
    config.write_text(original)
    Installer(tmp_path).codex()
    assert config.read_text() == original
    installer = Installer(tmp_path, True)
    installer.codex()
    assert tomllib.loads(config.read_text())['tui'] == {'animations': False, 'theme': 'ithilien-dawn'}
    assert next(installer.backup.rglob('config.toml')).read_text() == original
    count = installer.count
    installer.codex()
    assert installer.count == count
