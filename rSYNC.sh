#!/usr/bin/env bash
#
export SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )";
export SCRIPT_NAME=$(basename "$0");

export REMOTE_PROJECT_DIR="returnable";

source ${HOME}/projects/FacElect/install_scripts/envars.sh;

export REMOTE_PROJECT="${SERVER_ALIAS}:/home/${ERP_USER}/${TARGET_BENCH_NAME}/apps/${REMOTE_PROJECT_DIR}";

echo -e "Synching this directory '$(pwd)' with :: ${REMOTE_PROJECT}";

# exit;

while inotifywait -qqr -e close_write,move,create,delete ./*; do
  rsync -rzavx --update . ${REMOTE_PROJECT};
done;

  # echo -e "\n\n/* ~~~~~~~~~ Curtailed ~~~~~~~ ${SCRIPT_DIR}/${SCRIPT_NAME} ~~~~~~~~ */

  # ";
  # exit;
