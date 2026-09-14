# Shared Dawn/Dusk prompt: muted user and hostname, blue path, purple Git.
# Keep the user's existing vcs_info/precmd hooks; use a literal newline.
setopt PROMPT_SUBST
export PS1='%F{8}%n@%m%f:%F{blue}%~%f %F{magenta}${vcs_info_msg_0_}%f
%f$ '
