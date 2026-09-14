# Follow the terminal palette directly, including Ghostty light/dark changes.
# Remove the former macOS preference polling hook when upgrading a live shell.
autoload -Uz add-zsh-hook
add-zsh-hook -d precmd _ithilien_update_appearance
unfunction _ithilien_update_appearance 2>/dev/null
unset _ITHILIEN_SHELL_VARIANT _ITHILIEN_SHELL_DIR
source "${${(%):-%x}:A:h}/ithilien-auto.zsh"
