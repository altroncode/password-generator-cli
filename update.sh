#!/usr/bin/env bash

shopt -s extglob
shopt -s dotglob

if [[ -d .git ]]; then
  echo "Installation must not take place in the development directory. Use install.sh instead"
  exit 1
fi

external_launch=false

while getopts "x" opt; do
  case ${opt} in
  x)
    external_launch=true
    ;;
  \?)
    echo -e "${RED}Wrong flag: -$OPTARG${RESET}"
    exit 1
    ;;
  esac
done

current_directory=$(dirname "$0")
source_directory_name=$(uuidgen)
temporary_installation_directory_name=$(uuidgen)
config_file_path=${current_directory}/config/settings.ini

if $external_launch; then
  new_config_path=$config_file_path
  return
fi

chmod +x "$current_directory"/update.sh

git clone https://github.com/altroncode/password-generator-cli.git "$source_directory_name"

cp "$config_file_path" "$current_directory"

rm -rv !("$source_directory_name"|.env|settings.ini)
bash "$current_directory/$source_directory_name/install.sh" \
 "$current_directory/$temporary_installation_directory_name" -l

# shellcheck disable=SC1090
source "$current_directory/$temporary_installation_directory_name/update.sh" -x

mv "$current_directory"/"$(basename "$config_file_path")" "$new_config_path.old"

rm "$current_directory/$temporary_installation_directory_name/.env"
mv "$current_directory/$temporary_installation_directory_name/*" "$current_directory"
