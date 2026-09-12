"""Apply the stock Codex motion setting without rewriting unrelated TOML."""
import copy
import re
import tomllib
from pathlib import Path

PROFILE = Path(__file__).resolve().parents[1] / 'extras/codex/config.toml'


def animations_enabled():
    return tomllib.loads(PROFILE.read_text())['tui']['animations']


def configure(text):
    before = tomllib.loads(text)
    enabled = animations_enabled()
    if before.get('tui', {}).get('animations') is enabled:
        return text
    value = str(enabled).lower()
    lines = text.splitlines(keepends=True)
    section = None
    insertion = None
    replaced = False
    for i, line in enumerate(lines):
        header = re.match(r'^\s*\[\s*(tui|"tui"|\'tui\')\s*\]\s*(?:#.*)?$', line.strip())
        if header:
            section = 'tui'
            insertion = i + 1
        elif line.lstrip().startswith('['):
            section = 'other'
        key = r'(?:animations|"animations"|\'animations\')' if section == 'tui' else r'tui\s*\.\s*animations' if section is None else r'(?!)'
        match = re.match(r'^(\s*' + key + r'\s*=\s*)(true|false)(\s*(?:#.*)?)$', line.rstrip('\n'))
        if match:
            lines[i] = match[1] + value + match[3] + ('\n' if line.endswith('\n') else '')
            replaced = True
    if replaced:
        result = ''.join(lines)
    elif 'animations' in before.get('tui', {}):
        raise ValueError('Unsupported TOML spelling for tui.animations; no config was changed')
    elif insertion is not None:
        lines[insertion - 1] = lines[insertion - 1].rstrip('\n') + '\n'
        lines.insert(insertion, f'animations = {value}\n')
        result = ''.join(lines)
    elif 'tui' not in before:
        result = text.rstrip() + f'\n\n[tui]\nanimations = {value}\n'
    else:
        # A root dotted key can extend an existing dotted-key table.
        result = f'tui.animations = {value}\n' + text
    expected = copy.deepcopy(before)
    expected.setdefault('tui', {})['animations'] = enabled
    if tomllib.loads(result) != expected:
        raise ValueError('Codex config edit would change unrelated settings')
    return result
