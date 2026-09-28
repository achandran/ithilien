# Generated terminal-relative Ithilien colors; requires the Ithilien terminal palette.
zle_highlight=("${(@)zle_highlight:#region:*}" "region:bg=#8D9563,fg=#000000")
# Remove inherited fixed palettes too, including shells without the old marker.
() {
    local previous
    for previous in "${_ITHILIEN_FZF_COLORS-}" '--color=light,bg:#FAFAF8,fg:#000000,bg+:#8D9563,fg+:#000000,hl:#000000:underline,hl+:#000000:underline,info:#000000,header:#000000,border:#545350,prompt:#8B3037,pointer:#000000,marker:#000000,spinner:#8B3037,gutter:#FAFAF8,query:#000000' '--color=dark,bg:#1E1F19,fg:#BDB7AB,bg+:#8D9563,fg+:#000000,hl:#BDB7AB:underline,hl+:#000000:underline,info:#BDB7AB,header:#BDB7AB,border:#AAA497,prompt:#E09A9D,pointer:#000000,marker:#BDB7AB,spinner:#E09A9D,gutter:#1E1F19,query:#BDB7AB' '--color=16,bg:-1,fg:-1,bg+:#8D9563,fg+:#000000,hl:-1:underline,hl+:#000000:underline,info:-1,header:-1,border:8,prompt:1,pointer:#000000,marker:-1,spinner:1,gutter:-1,query:-1'; do
        [[ -n $previous ]] || continue
        FZF_DEFAULT_OPTS=${FZF_DEFAULT_OPTS//"$previous"/}
        FZF_CTRL_R_OPTS=${FZF_CTRL_R_OPTS//"$previous"/}
    done
}
export _ITHILIEN_FZF_COLORS='--color=16,bg:-1,fg:-1,bg+:#8D9563,fg+:#000000,hl:-1:underline,hl+:#000000:underline,info:-1,header:-1,border:8,prompt:1,pointer:#000000,marker:-1,spinner:1,gutter:-1,query:-1'
export FZF_DEFAULT_OPTS="${FZF_DEFAULT_OPTS% } $_ITHILIEN_FZF_COLORS"
export FZF_CTRL_R_OPTS="${FZF_CTRL_R_OPTS% } $_ITHILIEN_FZF_COLORS"
