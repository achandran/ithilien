# Ithilien ZLE visual selection — generated; do not edit by hand.
zle_highlight=("${(@)zle_highlight:#region:*}" "region:bg=#8D9563,fg=#000000")

# fzf, including Ctrl-R history; safe to source repeatedly.
if [[ -n ${_ITHILIEN_FZF_COLORS-} ]]; then
  FZF_DEFAULT_OPTS=${FZF_DEFAULT_OPTS//"$_ITHILIEN_FZF_COLORS"/}
  FZF_CTRL_R_OPTS=${FZF_CTRL_R_OPTS//"$_ITHILIEN_FZF_COLORS"/}
fi
_ITHILIEN_FZF_COLORS='--color=dark,bg:#22201B,fg:#CCBC9E,bg+:#8D9563,fg+:#000000,hl:#CCBC9E:underline,hl+:#000000:underline,info:#CCBC9E,header:#CCBC9E,border:#AFA08F,prompt:#E09A9D,pointer:#000000,marker:#CCBC9E,spinner:#E09A9D,gutter:#22201B,query:#CCBC9E'
export FZF_DEFAULT_OPTS="${FZF_DEFAULT_OPTS% } $_ITHILIEN_FZF_COLORS"
export FZF_CTRL_R_OPTS="${FZF_CTRL_R_OPTS% } $_ITHILIEN_FZF_COLORS"
