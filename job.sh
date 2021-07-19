#!/usr/bin/env bash
#

# echo -e "Use DataPump on :  # 'S|Stock_Entry'";
# exit;

sleep 1;

if [[ ! -f envars.sh ]]; then
	# echo -e "Found NO symbolic link 'envars.sh' to an environment variables file.";
	ln -sf ../electronic_invoice/install_scripts/envars.sh envars.sh;
	# cat envars.sh;
fi;

source  envars.sh;
declare PRCTL="https";
declare DOCTYPE="${PRCTL}://${TARGET_HOST}/api/method/returnable.returnable.doctype.returnable";

declare AUTHZ="Authorization: token ${KEYS}";

declare PYTHON_FILE="";
declare EP_NAME="";
declare TGT="";

PYTHON_FILE="${DOCTYPE}.initialize_stock";
# EP_NAME="initializeStock";
EP_NAME="queueInitializeStock";
# EP_NAME="tester";

TGT="/dev/shm/initialize_stock.html";

declare Marcelo=0;
if [[ ${Marcelo} -eq 1 ]]; then
	echo -e "Processing Marcelo's loads...";
	PYTHON_FILE="${DOCTYPE}.getMarcelozItems";
	TGT="/dev/shm/getMarcelozItems.html";
	EP_NAME="loadItems";
fi;


echo -e "---------------------------------------------------------\n\n"
echo -e "Calling ${PYTHON_FILE}.${EP_NAME}\n  with ${AUTHZ}\n  to ${TGT}\n------\n";
# exit;

curl -s -L -X POST "${PYTHON_FILE}.${EP_NAME}" \
-H "${AUTHZ}" \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'company=Logichem Solutions S. A.' > ${TGT}
jq -r '.message' ${TGT};

exit;

