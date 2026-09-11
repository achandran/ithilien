# Ithilien ZLE visual selection — generated; do not edit by hand.
zle_highlight=("${(@)zle_highlight:#region:*}" "region:bg=#8B3037,fg=#FFFFFF")

# fzf, including Ctrl-R history; safe to source repeatedly.
if [[ -n ${_ITHILIEN_FZF_COLORS-} ]]; then
  FZF_DEFAULT_OPTS=${FZF_DEFAULT_OPTS//"$_ITHILIEN_FZF_COLORS"/}
  FZF_CTRL_R_OPTS=${FZF_CTRL_R_OPTS//"$_ITHILIEN_FZF_COLORS"/}
fi
_ITHILIEN_FZF_COLORS='--color=light,bg:#FAFAF8,fg:#000000,bg+:#8B3037,fg+:#FFFFFF,hl:#000000:underline,hl+:#FFFFFF:underline,info:#000000,header:#000000,border:#505456,prompt:#8B3037,pointer:#000000,marker:#000000,spinner:#8B3037,gutter:#FAFAF8,query:#000000'
export FZF_DEFAULT_OPTS="${FZF_DEFAULT_OPTS% } $_ITHILIEN_FZF_COLORS"
export FZF_CTRL_R_OPTS="${FZF_CTRL_R_OPTS% } $_ITHILIEN_FZF_COLORS"
