#!/usr/bin/env bash
#
sleep 3;

export ROW_COUNT="";
callHost() {
	# echo curl -s -L -X POST "${ENDPOINT}.${EP_NAME}" \
	# -H "${AUTHZ}" \
	# -H 'Content-Type: application/x-www-form-urlencoded' \
	# --data-urlencode 'company=Logichem Solutions S. A.'

	curl -s -L -X POST "${ENDPOINT}.${EP_NAME}" \
	-H "${AUTHZ}" \
	-H 'Content-Type: application/x-www-form-urlencoded' \
	--data-urlencode 'company=Logichem Solutions S. A.' > ${TGT}
	# jq -r '.message' ${TGT};
	ROW_COUNT=$(tail -n 1 ${LOG});


	declare LIMIT=580;
	if (( ROW_COUNT < LIMIT )); then
		return 1;
	else
		echo -e "Counted ${ROW_COUNT} stock entries";
	fi;
}

if [[ -f envars.sh ]]; then

	source  envars.sh;
	declare PRCTL="https";
	declare ENDPOINT="${PRCTL}://${TARGET_HOST}/api/method/returnable.returnable.doctype.returnable.returnable";

	echo -e "---------------------------------------------------------\n\n"
	echo -e "Calling ${ENDPOINT}\n------\n";

	declare TMP_DIR="/dev/shm/";
	declare LOG_DIR="${TMP_DIR}/erpnext";
	declare TGT="${TMP_DIR}/install_returnables.html";
	declare LOG="${LOG_DIR}/notification.log";

	mkdir -p "${LOG_DIR}";
	touch "${LOG_DIR}/notification.log";
	touch "${LOG_DIR}/result.log";

	declare EP_NAME="";
	# EP_NAME="installReturnables";
	EP_NAME="queueInstallReturnables";
	EP_NAME="se_count";
	EP_NAME="tester";


	declare ATTEMPT_COUNTER=0
	declare MAX_ATTEMPTS=3
	declare DELAY=5

	echo -e "Will try ${MAX_ATTEMPTS} times with a ${DELAY} second delay between tries.";

	until callHost; do
	    if [ ${ATTEMPT_COUNTER} -eq ${MAX_ATTEMPTS} ]; then
	      echo -e "\n\nMax attempts reached. Stock Entry process may have failed"
	      exit 1
	    fi

	    echo -e " - ${ROW_COUNT}"
	    ATTEMPT_COUNTER=$(($ATTEMPT_COUNTER+1))
	    sleep ${DELAY}
	done

else 
	echo -e "Found NO symbolic link 'envars.sh' to an environment variables file.";
fi;
exit;

# #!/usr/bin/env bash
# #
# # sleep 1;


# if [[ -f envars.sh ]]; then

# 	source  envars.sh;
# 	declare PRCTL="https";
# 	declare ENDPOINT="${PRCTL}://${TARGET_HOST}/api/method/returnable.returnable.doctype.returnable.returnable";

# 	echo -e "---------------------------------------------------------\n\n"
# 	echo -e "Calling ${ENDPOINT}\n------\n";

# 	declare TGT="/dev/shm/install_returnables.html";
# 	declare AUTHZ="Authorization: token ${KEYS}";

# 	declare EP_NAME="";
# 	# EP_NAME="installReturnables";
# 	EP_NAME="queueInstallReturnables";
# 	EP_NAME="tester";

# 	curl -s -L -X POST "${ENDPOINT}.${EP_NAME}" \
# 	-H "${AUTHZ}" \
# 	-H 'Content-Type: application/x-www-form-urlencoded' \
# 	--data-urlencode 'company=Logichem Solutions S. A.' > ${TGT}
# 	jq -r '.message' ${TGT};

# else 
# 	echo -e "Found NO symbolic link 'envars.sh' to an environment variables file.";
# fi;
# exit;

