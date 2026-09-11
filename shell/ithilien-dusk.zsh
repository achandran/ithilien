# Ithilien ZLE visual selection — generated; do not edit by hand.
zle_highlight=("${(@)zle_highlight:#region:*}" "region:bg=#B17232,fg=#000000")

# fzf, including Ctrl-R history; safe to source repeatedly.
if [[ -n ${_ITHILIEN_FZF_COLORS-} ]]; then
  FZF_DEFAULT_OPTS=${FZF_DEFAULT_OPTS//"$_ITHILIEN_FZF_COLORS"/}
  FZF_CTRL_R_OPTS=${FZF_CTRL_R_OPTS//"$_ITHILIEN_FZF_COLORS"/}
fi
_ITHILIEN_FZF_COLORS='--color=dark,bg:#171812,fg:#C9BA99,bg+:#B17232,fg+:#000000,hl:#C9BA99:underline,hl+:#000000:underline,info:#C9BA99,header:#C9BA99,border:#A09880,prompt:#DA8075,pointer:#000000,marker:#000000,spinner:#DA8075,gutter:#171812,query:#C9BA99'
export FZF_DEFAULT_OPTS="${FZF_DEFAULT_OPTS% } $_ITHILIEN_FZF_COLORS"
export FZF_CTRL_R_OPTS="${FZF_CTRL_R_OPTS% } $_ITHILIEN_FZF_COLORS"
