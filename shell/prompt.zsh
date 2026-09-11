# Ithilien Dawn prompt: graphite user, Rosehip hostname, blue path, purple Git.
# Keep the user's existing vcs_info/precmd hooks; use a literal newline.
setopt PROMPT_SUBST
export PS1='%F{black}%n%f@%F{9}%m%f:%F{blue}%~%f %F{magenta}${vcs_info_msg_0_}%f
%f$ '
