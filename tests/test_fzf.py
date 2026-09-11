"""Exercise generated fzf options through zsh, including variant switching."""
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which('zsh'), 'zsh required')
class FzfColors(unittest.TestCase):
    def test_preserve_options_and_replace_colors(self):
        script = r'''
        export FZF_DEFAULT_OPTS='--height=40%'
        export FZF_CTRL_R_OPTS='--preview "echo {}"'
        source shell/ithilien-dawn.zsh
        first=$FZF_DEFAULT_OPTS
        source shell/ithilien-dawn.zsh
        [[ $first == $FZF_DEFAULT_OPTS ]] || exit 1
        [[ $FZF_CTRL_R_OPTS == *'--preview "echo {}"'* ]] || exit 2
        source shell/ithilien-dusk.zsh
        source shell/ithilien-dawn.zsh
        [[ $first == $FZF_DEFAULT_OPTS ]] || exit 3
        [[ $FZF_DEFAULT_OPTS == *'bg+:#A8B2AE,fg+:#000000'* ]] || exit 4
        [[ $FZF_CTRL_R_OPTS == *'hl+:#000000:underline'* ]] || exit 5
        '''
        subprocess.run(['zsh', '-f', '-c', script], cwd=ROOT, check=True)
