# Choose the Claude Code theme once per launch from macOS appearance.
unalias ai 2>/dev/null
function ai() {
    local dark theme=ithilien-dawn

    dark=$(/usr/bin/osascript -e \
        'tell application "System Events" to tell appearance preferences to get dark mode') \
        || return

    [[ $dark == true ]] && theme=ithilien-dusk

    command claude --settings \
        "{\"theme\":\"custom:$theme\"}" "$@"
}
