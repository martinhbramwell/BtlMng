#!/usr/bin/env bash
#

export SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )";
export SCRIPT_NAME=$(basename "$0");

# source ${SCRIPT_DIR}/../FacElect/install_scripts/envars.sh
source ${HOME}/projects/FacElect/install_scripts/envars.sh

mkdir -p /dev/shm/erpnext_log/

echo -e "Wait";
sleep 1;

echo -e "Go";
curl -sLX POST "http://${ERPNEXT_SITE_URL}:8001/api/method/returnable.returnable.doctype.returnable.returnable.install_returnables" \
-H "Authorization: token ${KEYS}" \
-H "Content-Type: application/json"
echo -e "";

echo -e "/* ~~~~~~~~~ Curtailed ~~~~~~~ ${KEYS} ~~~~~~~~ */";
exit;

