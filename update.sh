#!/usr/bin/env bash

shopt -s extglob
shopt -s dotglob

RED='\033[0;31m'
RESET='\033[0m'

function update_config {
  local config_file_path=$1
  local old_config_path=$2
  mv "$old_config_path" "$(dirname "$config_file_path")/$(basename "$old_config_path").old"
}

if [[ -d .git ]]; then
  echo -e "${RED}Installation must take place in the development directory${RESET}"
  exit 1
fi

current_directory=$(dirname "$0")
source_directory_name=$(uuidgen)
temporary_installation_directory_name=$(uuidgen)
config_file_path=${current_directory}/config/settings.ini

while getopts ":c" opt; do
  case ${opt} in
  c)
    old_config_path="$OPTARG"
    echo "$old_config_path"
    update_config "$config_file_path" "$old_config_path"
    exit 0
    ;;
  \?)
    echo -e "${RED}Wrong flag: -$OPTARG${RESET}"
    exit 1
    ;;
  esac
done

chmod +x "$current_directory"/update.sh

git clone https://github.com/altroncode/password-generator-cli.git "$source_directory_name"

cp "$config_file_path" "$current_directory"

rm -rv !("$source_directory_name"|.env|settings.ini)
mkdir .git
bash "$current_directory/$source_directory_name/install.sh" \
 "$current_directory/$temporary_installation_directory_name" -l
rm -rf .git

bash "$current_directory/$temporary_installation_directory_name/update.sh" -c "$config_file_path"

#rm -rf "$current_directory/$temporary_installation_directory_name/.env"
#mv "$current_directory"/"$temporary_installation_directory_name"/* "$current_directory"
