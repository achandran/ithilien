#!/usr/bin/env python3
"""Install supported Ithilien integrations; standard library only."""
import argparse
from datetime import datetime, timezone
import os
import re
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def managed_config(text, theme):
    """Keep unrelated settings; replace active theme directives and our block."""
    start, end = '# BEGIN ITHILIEN', '# END ITHILIEN'
    lines, inside = [], False
    for line in text.splitlines():
        if line == start:
            if inside:
                raise ValueError('Nested Ithilien config block')
            inside = True
        elif line == end:
            if not inside:
                raise ValueError('Unmatched Ithilien config block')
            inside = False
        elif not inside and not re.match(r'^\s*theme\s*=', line):
            lines.append(line)
    if inside:
        raise ValueError('Unclosed Ithilien config block')
    return '\n'.join(lines).rstrip() + f'\n\n{start}\ntheme = {theme}\n{end}\n'


class Installer:
    def __init__(self, home, apply=False, only=None):
        self.home, self.apply, self.only = home, apply, only
        self.config = Path(os.environ.get('XDG_CONFIG_HOME', home / '.config'))
        self.backup = home / '.local/share/ithilien/backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        self.count = 0

    def detected(self, command, app):
        return bool(shutil.which(command) or any((p / f'{candidate}.app').exists() for p in [Path('/Applications'), self.home / 'Applications'] for candidate in ([app, 'Firefox Developer Edition', 'Firefox Nightly'] if app == 'Firefox' else [app])))

    def write(self, path, data):
        if path.is_symlink():
            raise ValueError(f'Refusing to replace symlink: {path}; update its source instead')
        if path.exists() and path.read_bytes() == data:
            print(f'UNCHANGED {path}')
            return
        print(f'{"WRITE" if self.apply else "WOULD WRITE"} {path}')
        if self.apply:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                dest = self.backup / str(path).lstrip('/')
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
            path.write_bytes(data)
        self.count += 1

    def copies(self, source, destination):
        for path in sorted((ROOT / source).iterdir()):
            if path.is_file():
                self.write(destination / path.name, path.read_bytes())

    def run(self):
        integrations = [('ghostty', 'Ghostty'), ('nvim', 'Neovim'), ('codex', 'Codex'), ('claude', 'Claude'), ('slack', 'Slack'), ('linear', 'Linear'), ('firefox', 'Firefox'), ('zsh', 'Zsh')]
        for command, app in integrations:
            if self.only and command not in self.only:
                continue
            if not self.detected(command, app):
                print(f'SKIP {app}: not detected')
                continue
            try:
                getattr(self, command)()
            except (OSError, ValueError) as error:
                print(f'ERROR {app}: {error}', file=sys.stderr)
                self.errors += 1
        if self.apply and self.backup.exists():
            print(f'Backups: {self.backup}')
        return bool(self.errors)

    errors = 0

    def ghostty(self):
        # Ghostty installation intentionally targets the user's .config folder.
        base = self.home / '.config/ghostty'
        config = base / 'config'
        self.copies('ghostty/themes', base / 'themes')
        text = config.read_text() if config.exists() else ''
        self.write(config, managed_config(text, 'light:ithilien_dawn.conf,dark:ithilien_dusk.conf').encode())
        print('NEXT Ghostty: reload configuration. Explicit cursor/font/contrast overrides in your config still take precedence over theme values.')

    def codex(self):
        self.copies('codex/themes', Path(os.environ.get('CODEX_HOME', self.home / '.codex')) / 'themes')
        print('NEXT Codex CLI: choose Ithilien Dawn using /theme. Desktop appearance is separate.')

    def claude(self):
        self.copies('claude-code/themes', Path(os.environ.get('CLAUDE_CONFIG_DIR', self.home / '.claude')) / 'themes')
        print('NEXT Claude Code: choose Ithilien Dawn using /theme; requires custom-theme support. Claude desktop is separate.')

    def nvim(self):
        base = self.config / os.environ.get('NVIM_APPNAME', 'nvim')
        files = list((base / 'lua').rglob('*.lua')) if (base / 'lua').exists() else []
        lazyvim = any('LazyVim/LazyVim' in p.read_text(errors='replace') for p in files)
        if not lazyvim:
            print('MANUAL Neovim: automatic activation supports LazyVim; see docs/installation.md for other configurations.')
            return
        # Local checkout ensures git pull + installer uses the exact revision.
        import json
        plugin = 'return {\n  { dir = ' + json.dumps(str(ROOT)) + ', name = "ithilien", lazy = false, priority = 1000,\n    dependencies = { "zenbones-theme/zenbones.nvim", "rktjmp/lush.nvim", "webhooked/kanso.nvim" },\n    config = function() vim.cmd.colorscheme("ithilien-dawn") end },\n  { "LazyVim/LazyVim", opts = { colorscheme = "ithilien-dawn" } },\n}\n'
        self.write(base / 'lua/plugins/ithilien-installed.lua', plugin.encode())
        print('NEXT Neovim: restart and run :Lazy sync for dependencies. Keep this checkout in place; remove conflicting theme specs if needed.')

    def slack(self):
        print('MANUAL Slack: import in Preferences > Appearance > Custom theme:\n' + (ROOT / 'slack/ithilien-dawn.txt').read_text().strip())

    def linear(self):
        print('MANUAL Linear: import in Settings > Interface and theme:\n' + (ROOT / 'linear/ithilien-dawn.txt').read_text().strip())

    def firefox(self):
        destination = self.home / '.local/share/ithilien/firefox'
        for variant in ('dawn', 'dusk'):
            self.copies(f'firefox/ithilien-{variant}', destination / f'ithilien-{variant}')
        print(f'MANUAL Firefox: about:debugging > This Firefox > Load Temporary Add-on; select {destination}/ithilien-dawn/manifest.json. Temporary themes expire on restart; permanent distribution needs Mozilla signing. This themes browser chrome, not website selections.')

    def zsh(self):
        destination = self.config / 'ithilien'
        for variant in ('dawn', 'dusk'):
            source = ROOT / 'shell' / f'ithilien-{variant}.zsh'
            self.write(destination / source.name, source.read_bytes())
        rc = Path(os.environ.get('ZDOTDIR') or self.home) / '.zshrc'
        text = rc.read_text() if rc.exists() else ''
        start, end = '# BEGIN ITHILIEN ZLE', '# END ITHILIEN ZLE'
        if (start in text) != (end in text):
            raise ValueError('Incomplete Ithilien ZLE block')
        text = re.sub(r'(?ms)^# BEGIN ITHILIEN ZLE\n.*?^# END ITHILIEN ZLE\n?', '', text)
        selection = (ROOT / "shell/ithilien-dawn.zsh").read_text().rstrip()
        block = f"{start}\n{selection}\n{end}\n"
        self.write(rc, (text.rstrip() + '\n\n' + block).encode())
        print('NEXT zsh: start a new shell. Dawn visual selection is installed; source ithilien-dusk.zsh instead for a dark terminal. Existing non-region ZLE styles are preserved.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Write changes; default is a dry run')
    parser.add_argument('--only', nargs='+', choices=['ghostty', 'nvim', 'codex', 'claude', 'slack', 'linear', 'firefox', 'zsh'])
    args = parser.parse_args()
    return Installer(Path.home(), args.apply, args.only).run()


if __name__ == '__main__':
    sys.exit(main())
