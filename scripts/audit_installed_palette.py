"""Audit installed Neovim plugins against Dawn's palette without updating plugins."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--nvim', default='nvim')
    parser.add_argument('--init', type=Path, default=Path.home()/'.config/nvim/init.lua')
    parser.add_argument('--lazy-root', type=Path, default=Path.home()/'.local/share/nvim/lazy/lazy.nvim')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not args.init.is_file() or not args.lazy_root.is_dir():
        parser.error('Installed Neovim config and lazy.nvim are required; coverage is unavailable.')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ithilien-plugin-audit-') as tmp:
        env = dict(os.environ, ITHILIEN_ROOT=str(ROOT), ITHILIEN_NVIM_INIT=str(args.init.resolve()),
                   ITHILIEN_LAZY_ROOT=str(args.lazy_root.resolve()), ITHILIEN_AUDIT_OUTPUT=str(output),
                   XDG_STATE_HOME=tmp+'/state', XDG_CACHE_HOME=tmp+'/cache')
        with (output/'nvim.log').open('w') as log:
            result = subprocess.run([args.nvim, '--headless', '-u', str(ROOT/'scripts/audit_installed_palette.lua'),
                                     '-i', 'NONE', '-n'], cwd=tmp, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=120)
    print(f"{'PASS' if result.returncode == 0 else 'FAIL'}: installed highlight audit; {output/'result.json'}")
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
