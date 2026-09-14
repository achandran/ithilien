# Choose the Codex theme once per launch from macOS appearance.
unalias ai 2>/dev/null
function ai() {
    local theme=ithilien-dawn
    if [[ "$(/usr/bin/defaults read -g AppleInterfaceStyle 2>/dev/null)" == Dark ]]; then
        theme=ithilien-dusk
    fi
    command codex -c "tui.theme=\"$theme\"" "$@"
}
