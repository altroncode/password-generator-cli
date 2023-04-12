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
shift

while getopts "fd" opt; do
  case ${opt} in
  f)
    force_mode=true
    ;;
  d)
    is_delete=true
    ;;
  \?)
    echo -e "${RED}Wrong flag: -$OPTARG${RESET}"
    exit 1
    ;;
  esac
done

if $is_delete; then
  rm -rf "$installation_path"
  unlink password-gen
  exit 0
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

ln -sf "$installation_path"/__main__.py ~/.local/bin/password-gen
