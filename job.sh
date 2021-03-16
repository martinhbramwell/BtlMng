#!/usr/bin/env bash
#

sleep 4;


if [[ -f envars.sh ]]; then

	source  envars.sh;
	declare PRCTL="https";
	declare ENDPOINT="${PRCTL}://${TARGET_HOST}/api/method/returnable.returnable.doctype.returnable.returnable";

	echo -e "---------------------------------------------------------\n\n"
	echo -e "Calling ${ENDPOINT}\n------\n";

	declare TGT="/dev/shm/install_returnables.html";
	declare AUTHZ="Authorization: token ${KEYS}";

	declare EP_NAME="";
	# EP_NAME="installReturnables";
	EP_NAME="tester";
	EP_NAME="queueInstallReturnables";

	curl -s -L -X POST "${ENDPOINT}.${EP_NAME}" \
	-H "${AUTHZ}" \
	-H 'Content-Type: application/x-www-form-urlencoded' \
	--data-urlencode 'company=Logichem Solutions S. A.' > ${TGT}
	jq -r '.message' ${TGT};

else 
	echo -e "Found NO symbolic link 'envars.sh' to an environment variables file.";
fi;
exit;

