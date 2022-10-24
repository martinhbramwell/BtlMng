export YOUR_HOST="https://dev.logichem.solutions";
export YOUR_TOKEN="56435adde957d7f:63d3bd0241716c5";
export YOUR_SERIES="Returnable Movement";
export YOUR_TEMPLATE="RET-MOV-.#########";
export CURR_VALUE="1";

export REST_ENDPOINT="${YOUR_HOST}/api/resource";
export RPC_ENDPOINT="${YOUR_HOST}/api/method";
export DATE_MODIFIED=$(curl -s "${REST_ENDPOINT}/Naming%20Series/Naming%20Series" -H "Authorization: token ${YOUR_TOKEN}" | jq -r .data.modified);

echo ${DATE_MODIFIED}


cat << NSEOF > /dev/shm/SeriesSpec.json;
{
    "method": "get_options",
    "docs": "{\"name\":\"Naming Series\",\"doctype\":\"Naming Series\",\"select_doc_for_series\":\"${YOUR_SERIES}\",\"modified\":\"${DATE_MODIFIED}\"}"
}
NSEOF

cat /dev/shm/SeriesSpec.json;


curl -sX POST "${RPC_ENDPOINT}/runserverobj" \
  -H "Authorization: token ${YOUR_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/dev/shm/SeriesSpec.json > /dev/shm/OldSeries.json;

export OLD_TEMPLATES=$(cat /dev/shm/OldSeries.json | jq -r .);

echo -e "
Existing templates:
${OLD_TEMPLATES}
";

cat << UPEOF > /dev/shm/SeriesUpdate.json;
{
     "method": "update_series",
     "docs": "{\"name\":\"Naming Series\",\"doctype\":\"Naming Series\",\"select_doc_for_series\":\"${YOUR_SERIES}\",\"set_options\":\"\\\n${YOUR_TEMPLATE}\",\"modified\":\"${DATE_MODIFIED}\"}"
}
UPEOF

cat /dev/shm/SeriesUpdate.json;

curl -sX POST "${RPC_ENDPOINT}/runserverobj" \
  -H "Authorization: token ${YOUR_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/dev/shm/SeriesUpdate.json | jq -r .;



cat << SSEOF > /dev/shm/SeriesStartUpdate.json;
{
     "method": "update_series_start",
     "docs": "{\"doctype\":\"Naming Series\",\"docstatus\": 1,\"prefix\":\"${YOUR_TEMPLATE}\",\"current_value\":${CURR_VALUE},\"modified\":\"${DATE_MODIFIED}\"}"
}
SSEOF

curl -sX POST "${RPC_ENDPOINT}/runserverobj" \
--header "Authorization: token ${YOUR_TOKEN}" \
--header 'Content-Type: application/json' \
  -d @/dev/shm/SeriesStartUpdate.json | jq -r .;



