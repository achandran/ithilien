# Ithilien ZLE visual selection — generated; do not edit by hand.
zle_highlight=("${(@)zle_highlight:#region:*}" "region:bg=#B8595C,fg=#000000")

# fzf, including Ctrl-R history; safe to source repeatedly.
if [[ -n ${_ITHILIEN_FZF_COLORS-} ]]; then
  FZF_DEFAULT_OPTS=${FZF_DEFAULT_OPTS//"$_ITHILIEN_FZF_COLORS"/}
  FZF_CTRL_R_OPTS=${FZF_CTRL_R_OPTS//"$_ITHILIEN_FZF_COLORS"/}
fi
_ITHILIEN_FZF_COLORS='--color=dark,bg:#202120,fg:#BDB7AB,bg+:#B8595C,fg+:#000000,hl:#BDB7AB:underline,hl+:#000000:underline,info:#BDB7AB,header:#BDB7AB,border:#AAA497,prompt:#E09A9D,pointer:#000000,marker:#BDB7AB,spinner:#E09A9D,gutter:#202120,query:#BDB7AB'
export FZF_DEFAULT_OPTS="${FZF_DEFAULT_OPTS% } $_ITHILIEN_FZF_COLORS"
export FZF_CTRL_R_OPTS="${FZF_CTRL_R_OPTS% } $_ITHILIEN_FZF_COLORS"
