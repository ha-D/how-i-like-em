getscreen() {
  name=$(echo ${STY} | sed -e 's/[0-9]*\.//g')
  if [[ -z "${name// }" ]]; then
    echo ""
  else
    echo "${name}."
  fi
}

getuser() {
  name=$(whoami)
  if [ "$name" = "root" ]; then
    echo "root."
  fi
}

PROMPT="%{$fg[green]%}$(getscreen)%{$fg_bold[red]%}$(getuser)%{$fg[green]%}$HOST %(?:%{$fg_bold[green]%}➜ :%{$fg_bold[red]%}➜ )"
PROMPT+=' %{$fg[cyan]%}%c%{$reset_color%} $(git_prompt_info)'

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}git:(%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%} "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%}) %{$fg[yellow]%}✗"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%})"
