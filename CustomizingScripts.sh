#!/usr/bin/env bash
#
declare SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )";
declare SCRATCH_DIR="/dev/shm";

declare SCRIPT_TARGET_FILE_NAME="";
declare SCRIPT_TARGET="";
declare SCRIPT_TARGET_DOC_TYPE="";

declare WRAPPED_JSON="";
declare JSON_BODY_FILE="";

source envars.sh;

declare PRCTL="https";
declare ERPN_API="${PRCTL}://${ERPNEXT_SITE_URL}/api";
declare RSRC_API="${ERPN_API}/resource";

declare AUTHZ="Authorization: token ${KEYS}";
declare MIME="Content-Type: application/json";

declare SCRIPT_PK="";



function wrapForJson() {
    declare EXECUTABLE=${1}

    echo -e "wrapForJson ${EXECUTABLE}  > ${SCRATCH_DIR}/tmp1.json * * * ";

    sed -E ':a;N;$!ba;s/\r{0,1}\n/\\n/g' ${EXECUTABLE} > ${SCRATCH_DIR}/tmp1.json;
    sed "s/\"/\\\\\"/g" ${SCRATCH_DIR}/tmp1.json | head -c -1 > ${SCRATCH_DIR}/tmp2.json

    WRAPPED_JSON=$(cat ${SCRATCH_DIR}/tmp2.json);
}

function parseName() {
    declare EXECUTABLE=${1}


    SCRIPT_TARGET_FILE_NAME="${EXECUTABLE#"${PFIX}"}";
    echo "${SCRIPT_TARGET_FILE_NAME}";
    SCRIPT_TARGET="${SCRIPT_TARGET_FILE_NAME%".${FILE_EXT}"}";
    TMP=($(echo ${SCRIPT_TARGET} | tr '-' ' '))

    SCRIPT_TARGET_DOC_TYPE="${TMP[0]//_/ }";
    if [[ ${SCRIPT_TYPE} = "Server" ]]; then
        SCRIPT_TARGET_EVENT_TYPE="${TMP[1]//_/ }";
        SCRIPT_PK="${SCRIPT_TARGET_DOC_TYPE} ${SCRIPT_TARGET_EVENT_TYPE}";
    else
        SCRIPT_PK="${SCRIPT_TARGET_DOC_TYPE}-Form";
    fi;
    echo -e "===> ${SCRIPT_PK} * * * ";
}

function buildPayload() {
    JSON_BODY_FILE="${SCRATCH_DIR}/${SCRIPT_TARGET}.json";
    if [[ ${SCRIPT_TYPE} = "Server" ]]; then
        echo -e " - reference_doctype:  ${SCRIPT_TARGET_DOC_TYPE}, \n       doctype_event:  ${SCRIPT_TARGET_EVENT_TYPE}";
        cat << SRVEOF > ${JSON_BODY_FILE}
{
    "doctype": "Server Script",
    "enabled": 1,
    "name": "${SCRIPT_TARGET_DOC_TYPE} ${SCRIPT_TARGET_EVENT_TYPE}",
    "doctype_event": "${SCRIPT_TARGET_EVENT_TYPE}",
    "reference_doctype": "${SCRIPT_TARGET_DOC_TYPE}",
    "script": "${WRAPPED_JSON}"
}
SRVEOF

    else
        echo -e " - dt:  ${SCRIPT_TARGET_DOC_TYPE}";
        cat << CLIEOF > ${JSON_BODY_FILE}
{
    "doctype": "Client Script",
    "enabled": 1,
    "dt": "${SCRIPT_TARGET_DOC_TYPE}",
    "script": "${WRAPPED_JSON}"
}
CLIEOF
    fi;
}

function deliverPayload() {
    echo -e "
    ----------------------------------";

    declare SCPK=$(echo ${SCRIPT_PK} | sed "s/ /%20/g")
    echo -e "curl -L -X DELETE \"${ENDPOINT}/${SCPK}\" -H \"${AUTHZ}\" -H \"${MIME}\"";
    curl -L -X DELETE "${ENDPOINT}/${SCPK}" -H "${AUTHZ}" -H "${MIME}";

    echo -e "\ncurl -L -X POST \"${ENDPOINT}\" -H \"${AUTHZ}\" -H \"${MIME}\" -d @${JSON_BODY_FILE}\n";
    curl -L -X POST "${ENDPOINT}" -H "${AUTHZ}" -H "${MIME}" -d @${JSON_BODY_FILE};

    echo -e "
    ----------------------------------";
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ -z ${1} ]]; then
        echo -e "Usage:   ./CustomizingScripts.sh [Server|Client] [name of a specific script]";
        exit;
    fi

    declare SCRIPT_TYPE=${1};
    declare DESIRED_SCRIPT=${2};
    declare SCRIPTS="";
    declare PFIX="CustScr_";
    declare FILE_EXT=;

    declare ENDPOINT="${RSRC_API}/${SCRIPT_TYPE}%20Script";

    echo -e "\n----------------------------------";
    echo -e "${ENDPOINT}";


    if [[ ${SCRIPT_TYPE} = "Server" ]]; then
        FILE_EXT="py";
    else
        FILE_EXT="js";
    fi;

    SCRIPTS="${SCRIPT_DIR}/returnable/returnable/app_scripts/${SCRIPT_TYPE}";


    pushd ${SCRIPTS} >/dev/null;
        echo -e "Will submit './${PFIX}*-${SCRIPT_TYPE}.${FILE_EXT}\n";
        # pwd;
        # exit;
        for SCRIPT_FILE in "${PFIX}"*-${SCRIPT_TYPE}.${FILE_EXT}
        do
            # echo -e "SCRIPT_FILE :: ${SCRIPT_FILE}"
            if [ -f "${SCRIPT_FILE}" ]; then

                # echo -e "wrapForJson ${SCRIPT_FILE}";
                # exit;

                # if [[ "${SCRIPT_FILE}" == "CustScr_Stock_Entry-Client.js" || "${SCRIPT_FILE}" == "CustScr_Stock_Entry-Before_Submit-Server.py" ]]; then
                # if [[ "${SCRIPT_FILE}" == "CustScr_Stock_Entry-After_Save-Server.py" ]]; then
                # if [[ "${SCRIPT_FILE}" == "CustScr_Stock_Entry-Client.js" || "${SCRIPT_FILE}" == "CustScr_Stock_Entry-After_Submit-Server.py" ]]; then
                if [[ "${SCRIPT_FILE}" == "${DESIRED_SCRIPT}" ]]; then
                    echo -e "Processing ${SCRIPT_FILE} * * * ";

                    wrapForJson ${SCRIPT_FILE};

                    parseName ${SCRIPT_FILE};

                    buildPayload;

                    echo -e "JSON_BODY_FILE :: ${JSON_BODY_FILE} * * * ";
                    deliverPayload;

                else
                    echo -e "* * * Skipped ${SCRIPT_FILE} * * * ";
                fi;

            fi

        done
        # echo -e "**********************  CURTAILED  *************************";
        # exit;
    popd >/dev/null;


fi;
