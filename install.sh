#!/usr/bin/env bash

set -Eeuo pipefail

RED='\033[0;31m'
RESET='\033[0m'

source_path=$(dirname "$0")
chmod +x "$source_path"/install.sh

if [ $# -lt 1 ]; then
  echo -e "${RED}No installation path${RESET}"
  exit 1
fi

installation_path=$1

force_mode=false
is_delete=false
is_local_installation=false
shift

while getopts "fdl" opt; do
  case ${opt} in
  f)
    force_mode=true
    ;;
  d)
    is_delete=true
    ;;
  l)
    is_local_installation=true
    ;;
  \?)
    echo -e "${RED}Wrong flag: -$OPTARG${RESET}"
    exit 1
    ;;
  esac
done

if $is_delete; then
  rm -rf "$installation_path"
  if [ -L ~/.local/bin/password-gen ]; then
    unlink ~/.local/bin/password-gen
  fi
  exit 0
fi

if ! [[ -d .git ]]; then
  echo -e "${RED}Installation must take place in the development directory${RESET}"
  exit 1
fi

if [[ -d "$installation_path" ]] && ! $force_mode; then
  echo -e "${RED}Directory already exists${RESET}"
  exit 1
elif [[ -d "$installation_path" ]]; then
  rm -rf "$installation_path"
fi

cp -r "$source_path/src" "$installation_path"
cp "$source_path"/.env.dist "$installation_path"
cp "$source_path"/README.md "$installation_path"
cp "$source_path/install.sh" "$installation_path"
cp "$source_path/update.sh" "$installation_path"

if ! [[ -e "$installation_path"/.env ]]; then
  while IFS= read -r line; do
    key=$(echo "$line" | awk '{print $1}')
    echo "${key%?}"= >> "$installation_path"/.env
  done < "$source_path"/.env.dist
fi

chmod +x "$installation_path"/__main__.py

if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  case $(basename "$SHELL") in
  "zsh")
    echo "export PATH=\$PATH:\$HOME/.local/bin" >>~/.zshrc
    ;;
  "bash")
    echo "export PATH=\$PATH:\$HOME/.local/bin" >>~/.bashrc
    ;;
  esac
fi

if ! [[ -d ~/.local/bin ]]; then
  mkdir ~/.local/bin
fi

if ! [[ $is_local_installation ]]; then
  ln -sf "$installation_path"/__main__.py ~/.local/bin/password-gen
fi
