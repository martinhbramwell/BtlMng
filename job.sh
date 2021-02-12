#!/usr/bin/env bash
#

sleep 1;


if [[ -f envars.sh ]]; then

	source  envars.sh;
	declare PRCTL="https";
	declare ENDPOINT="${PRCTL}://${TARGET_HOST}/api/method/returnable.returnable.doctype.returnable.returnable";


	declare TGT="/dev/shm/install_returnables.html";
	declare AUTHZ="Authorization: token ${KEYS}";

	# declare EP_NAME="installReturnables";
	declare EP_NAME="tester";

	> ${TGT}

	echo -e "Calling ${ENDPOINT}.${EP_NAME}";
	curl -s -L -X POST "${ENDPOINT}.${EP_NAME}" \
	-H "${AUTHZ}" \
	-H 'Content-Type: application/x-www-form-urlencoded' \
	--data-urlencode 'company=Logichem Solutions S. A.' > ${TGT}
	jq -er '.message' ${TGT} || cat ${TGT};
else 
	echo -e "Found NO symbolic link 'envars.sh' to an environment variables file.";
fi;
exit;

