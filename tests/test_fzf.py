"""Exercise generated fzf options through zsh, including repeated sourcing."""
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which('zsh'), 'zsh required')
class FzfColors(unittest.TestCase):
    def test_terminal_relative_colors_and_inherited_options(self):
        script = r'''
        export FZF_DEFAULT_OPTS='--height=40%'
        export FZF_CTRL_R_OPTS='--preview "echo {}"'
        source extras/shell/ithilien-dawn.zsh
        unset _ITHILIEN_FZF_COLORS
        source extras/shell/ithilien-dawn.zsh
        unset _ITHILIEN_FZF_COLORS
        source extras/shell/ithilien-dusk.zsh
        unset _ITHILIEN_FZF_COLORS
        existing_hook() { :; }
        _ithilien_update_appearance() { return 1; }
        precmd_functions=(existing_hook _ithilien_update_appearance)
        zle_highlight=('paste:standout')
        source extras/shell/auto.zsh
        [[ $precmd_functions == existing_hook ]] || exit 1
        [[ $FZF_DEFAULT_OPTS != *'--color=light,'* ]] || exit 2
        [[ $FZF_DEFAULT_OPTS != *'--color=dark,'* ]] || exit 3
        [[ $FZF_DEFAULT_OPTS == *'bg:-1,fg:-1,'* ]] || exit 4
        [[ $FZF_DEFAULT_OPTS == *'border:8,prompt:1,'* ]] || exit 5
        [[ $FZF_CTRL_R_OPTS == *'--preview "echo {}"'* ]] || exit 6
        [[ $FZF_DEFAULT_OPTS == *'--height=40%'* ]] || exit 7
        [[ ${zle_highlight[1]} == paste:standout ]] || exit 8
        # A nested shell inherits both options and the cleanup marker.
        first=$FZF_DEFAULT_OPTS
        zsh -f -c 'source extras/shell/auto.zsh; [[ $FZF_DEFAULT_OPTS == "$1" ]]' zsh "$first" || exit 9
        source extras/shell/auto.zsh
        [[ $FZF_DEFAULT_OPTS == $first ]] || exit 10
        if (( $+commands[fzf] )); then
            print test | fzf --filter=test >/dev/null || exit 11
        fi
        '''
        subprocess.run(['zsh', '-f', '-c', script], cwd=ROOT, check=True)

    def test_preserve_options_and_replace_colors(self):
        script = r'''
        export FZF_DEFAULT_OPTS='--height=40%'
        export FZF_CTRL_R_OPTS='--preview "echo {}"'
        source extras/shell/ithilien-dawn.zsh
        first=$FZF_DEFAULT_OPTS
        source extras/shell/ithilien-dawn.zsh
        [[ $first == $FZF_DEFAULT_OPTS ]] || exit 1
        [[ $FZF_CTRL_R_OPTS == *'--preview "echo {}"'* ]] || exit 2
        source extras/shell/ithilien-dusk.zsh
        source extras/shell/ithilien-dawn.zsh
        [[ $first == $FZF_DEFAULT_OPTS ]] || exit 3
        [[ $FZF_DEFAULT_OPTS == *'bg+:#B8595C,fg+:#000000'* ]] || exit 4
        [[ $FZF_CTRL_R_OPTS == *'hl+:#000000:underline'* ]] || exit 5
        '''
        subprocess.run(['zsh', '-f', '-c', script], cwd=ROOT, check=True)


def test_all_generated_dawn_fzf_foregrounds_meet_contrast_floor():
    import sys
    sys.path.insert(0,str(ROOT/'scripts'))
    from tintprobe.evaluate_interactions import fzf_roles
    options=subprocess.check_output(['zsh','-f','-c','source extras/shell/ithilien-dawn.zsh; print -rn -- "$FZF_CTRL_R_OPTS"'],cwd=ROOT,text=True)
    roles=fzf_roles(options)
    assert roles['prompt']['foreground']=='#8B3037'
    assert roles['spinner']['foreground']=='#8B3037'
    assert all(role['pass'] for role in roles.values())
    assert roles['fg+']['background']=='#B8595C'
