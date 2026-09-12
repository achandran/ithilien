#!/usr/bin/env python3
"""Install supported Ithilien integrations; standard library only."""
import argparse
import configparser
import json
import subprocess
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
        if command == 'macos':
            return sys.platform == 'darwin'
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
        integrations = [('ghostty', 'Ghostty'), ('nvim', 'Neovim'), ('codex', 'Codex'), ('claude', 'Claude'), ('slack', 'Slack'), ('linear', 'Linear'), ('firefox', 'Firefox'), ('zsh', 'Zsh'), ('macos', 'macOS')]
        for command, app in integrations:
            if self.only and command not in self.only:
                continue
            if not self.detected(command, app):
                print(f'SKIP {app}: not detected')
                continue
            try:
                getattr(self, command)()
            except (OSError, ValueError, subprocess.CalledProcessError) as error:
                print(f'ERROR {app}: {error}', file=sys.stderr)
                self.errors += 1
        if self.apply and self.backup.exists():
            print(f'Backups: {self.backup}')
        return bool(self.errors)

    errors = 0

    def macos(self):
        if sys.platform != 'darwin':
            print('SKIP macOS: not detected')
            return
        palette = json.loads((ROOT / 'palette/ithilien-dawn.json').read_text())
        color = palette['colors'][palette['highlight']['background']]
        value = ' '.join(f'{int(color[i:i+2], 16) / 255:.6f}' for i in (1, 3, 5)) + ' Other'
        current = subprocess.run(['/usr/bin/defaults', 'read', '-g', 'AppleHighlightColor'],
                                 capture_output=True, text=True)
        previous = current.stdout.strip() if current.returncode == 0 else None
        if previous == value:
            print('UNCHANGED macOS system highlight')
            return
        if not self.apply:
            print(f'WOULD WRITE macOS system highlight: {color}')
        if self.apply:
            self.backup.mkdir(parents=True, exist_ok=True)
            (self.backup / 'macos-highlight.json').write_text(json.dumps(
                {'domain': 'NSGlobalDomain', 'key': 'AppleHighlightColor', 'previous': previous}, indent=2) + '\n')
            subprocess.run(['/usr/bin/defaults', 'write', '-g', 'AppleHighlightColor', '-string', value], check=True)
            verified = subprocess.run(['/usr/bin/defaults', 'read', '-g', 'AppleHighlightColor'], capture_output=True, text=True)
            if verified.returncode != 0 or verified.stdout.strip() != value:
                raise ValueError(f'Highlight preference did not persist: expected {value!r}, read {verified.stdout.strip()!r}. Quit System Settings and retry.')
            print(f'VERIFIED macOS saved highlight preference: {color}')
            print('NEXT macOS: reopen System Settings to refresh its color picker; log out and back in if apps retain the old color. Live application rendering is not verified.')
        self.count += 1

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
        plugin = 'return {\n  { dir = ' + json.dumps(str(ROOT)) + ', name = "ithilien", lazy = false, priority = 1000,\n    dependencies = { "webhooked/kanso.nvim" },\n    config = function() vim.cmd.colorscheme("ithilien-dawn") end },\n  { "LazyVim/LazyVim", opts = { colorscheme = "ithilien-dawn" } },\n  { "nvim-lualine/lualine.nvim", opts = function(_, opts) require("ithilien.statusline").configure(opts) end },\n}\n'
        managed = base / 'lua/plugins/ithilien-installed.lua'
        existing = [p for p in files if p != managed and re.search(
            r"[\"']achandran/ithilien[\"']", p.read_text(errors='replace'))]
        if existing:
            print('UNCHANGED Neovim: existing Ithilien spec; update with :Lazy update.')
            if managed.exists():
                if managed.read_text() == plugin and not managed.is_symlink():
                    print(f'{"REMOVE" if self.apply else "WOULD REMOVE"} {managed}')
                    if self.apply:
                        dest = self.backup / str(managed).lstrip('/')
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(managed, dest)
                        managed.unlink()
                    self.count += 1
                else:
                    print(f'MANUAL Neovim: review customized duplicate {managed}; not removed.')
            return
        self.write(managed, plugin.encode())
        print('NEXT Neovim: restart and run :Lazy sync for dependencies. Keep this checkout in place; remove conflicting theme specs if needed.')

    def slack(self):
        print('MANUAL Slack: import in Preferences > Appearance > Custom theme:\n' + (ROOT / 'slack/ithilien-dawn.txt').read_text().strip())

    def linear(self):
        print('MANUAL Linear: import in Settings > Interface and theme:\n' + (ROOT / 'linear/ithilien-dawn.txt').read_text().strip())

    def firefox(self):
        destination = self.home / '.local/share/ithilien/firefox'
        for variant in ('dawn', 'dusk'):
            self.copies(f'firefox/ithilien-{variant}', destination / f'ithilien-{variant}')
        base = self.home / ('Library/Application Support/Firefox' if sys.platform == 'darwin' else '.mozilla/firefox')
        profiles = configparser.ConfigParser(interpolation=None)
        profiles.read(base / 'profiles.ini')
        selected = []
        for section in profiles.sections():
            if not section.startswith('Profile') or profiles.get(section, 'Name', fallback='') != 'dev-edition-default':
                continue
            path = Path(profiles.get(section, 'Path'))
            if profiles.get(section, 'IsRelative', fallback='1') == '1':
                path = base / path
            if path.is_dir() and path not in selected:
                selected.append(path)
        for profile in selected:
            css = (ROOT / 'firefox/ithilien-dawn/userContent.css').read_text().strip()
            for path, content in ((profile / 'chrome/userContent.css', css),
                                  (profile / 'user.js', 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);')):
                text = path.read_text() if path.exists() else ''
                start, end = '/* BEGIN ITHILIEN */', '/* END ITHILIEN */'
                if text.count(start) != text.count(end) or text.count(start) > 1 or (start in text and text.index(start) > text.index(end)):
                    raise ValueError(f'Malformed Ithilien block in {path}')
                text = re.sub(r'/\* BEGIN ITHILIEN \*/.*?/\* END ITHILIEN \*/\n?', '', text, flags=re.S)
                self.write(path, (text.rstrip() + '\n\n' + start + '\n' + content + '\n' + end + '\n').encode())
        if selected:
            print('NEXT Firefox Developer Edition: fully quit and reopen to activate Dawn webpage selections. Existing profile customizations are preserved.')
        else:
            print('SKIP Firefox profile selection: no dev-edition-default profile found; open Developer Edition once to create it. Renamed profiles require manual setup.')
        print(f'MANUAL Firefox: about:debugging > This Firefox > Load Temporary Add-on; select {destination}/ithilien-dawn/manifest.json. Temporary themes expire on restart; permanent distribution needs Mozilla signing. This add-on themes browser chrome; webpage selections are installed separately above.')

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
        prompt = (ROOT / "shell/prompt.zsh").read_text().rstrip()
        block = f"{start}\n{selection}\n{prompt}\n{end}\n"
        self.write(rc, (text.rstrip() + '\n\n' + block).encode())
        print('NEXT zsh: start a new shell. Dawn visual selection, fzf colors, and Ash user/hostname prompt are installed; source ithilien-dusk.zsh instead for a dark terminal. Existing non-region ZLE styles are preserved.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying them')
    parser.add_argument('--only', nargs='+', choices=['ghostty', 'nvim', 'codex', 'claude', 'slack', 'linear', 'firefox', 'zsh', 'macos'])
    args = parser.parse_args()
    return Installer(Path.home(), not args.dry_run, args.only).run()


if __name__ == '__main__':
    sys.exit(main())
