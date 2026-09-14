"""Keep standalone generation and the build wrapper on one preview pipeline."""
import runpy
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import generate_themes
import generate_preview
import palette_chart
from ithilienlib import ROOT


@pytest.mark.parametrize('preview_fails', [False, True])
def test_generation_refreshes_previews_after_ports_and_charts(monkeypatch, preview_fails):
    events = []
    for name in (
        'generate_ghostty', 'generate_neovim_palette', 'generate_codex_theme',
        'generate_claude_theme', 'generate_app_palettes', 'generate_neovim_default',
        'generate_shared_highlights', 'generate_auto_shell',
    ):
        monkeypatch.setattr(generate_themes, name,
                            lambda *args, _name=name, **kwargs: events.append(_name))
    monkeypatch.setattr(palette_chart, 'generate_chart',
                        lambda *args: events.append('chart'))

    def preview():
        events.append('preview')
        if preview_fails:
            raise RuntimeError('preview failed')

    monkeypatch.setattr(generate_preview, 'main', preview)
    if preview_fails:
        with pytest.raises(RuntimeError, match='preview failed'):
            generate_themes.main()
    else:
        generate_themes.main()
    assert events.count('generate_neovim_palette') == 2
    assert events[-3:] == ['chart', 'chart', 'preview']
    assert events.count('preview') == 1


def test_build_delegates_generation_without_a_second_preview(monkeypatch):
    import audit_palette
    import audit_dusk
    monkeypatch.setattr(audit_palette, 'main', Mock())
    monkeypatch.setattr(audit_dusk, 'main', Mock())
    preview = Mock()
    monkeypatch.setattr(generate_preview, 'main', preview)
    generate = Mock(side_effect=preview)
    monkeypatch.setattr(generate_themes, 'main', generate)
    runpy.run_path(str(ROOT / 'scripts/build.py'), run_name='__main__')
    generate.assert_called_once_with()
    preview.assert_called_once_with()
