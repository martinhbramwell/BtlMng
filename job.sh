#!/usr/bin/env bash
#

# sleep 1;

declare LOG_DIR="/dev/shm/erpnext";
declare LOG="${LOG_DIR}/result.log";

if [[ ! -f ${LOG} ]]; then
  mkdir -p ${LOG_DIR};
  > ${LOG};
fi;

if [[ -f envars.sh ]]; then

	source  envars.sh;





  # echo -e "bench --site ${SERVER_ADMIN_DOMAIN} execute returnable.returnable.doctype.returnable.cleanser.clean";
  bench --site ${SERVER_ADMIN_DOMAIN} execute returnable.returnable.doctype.returnable.cleanser.clean
  exit;

	# declare PRCTL="https";

	# declare TGT="/dev/shm/install_returnables.html";
	# declare AUTHZ="Authorization: token ${KEYS}";

	# # declare ENDPOINT="${PRCTL}://${TARGET_HOST}/api/method/returnable.returnable.doctype.returnable.returnable";
	# declare ENDPOINT="${PRCTL}://${TARGET_HOST}/api/method/returnable.returnable.doctype.returnable.cleanser";
	# # declare EP_NAME="installReturnables";
	# # declare EP_NAME="tester";
	# declare EP_NAME="clean";

	# > ${TGT}

	# echo -e "Calling ${ENDPOINT}.${EP_NAME}";
	# curl -s -L -X POST "${ENDPOINT}.${EP_NAME}" \
	# -H "${AUTHZ}" \
	# -H 'Content-Type: application/x-www-form-urlencoded' \
	# --data-urlencode 'company=Logichem Solutions S. A.' > ${TGT}
	# jq -er '.message' ${TGT} || cat ${TGT};
else 
	echo -e "Found NO symbolic link 'envars.sh' to an environment variables file.";
fi;
exit;

