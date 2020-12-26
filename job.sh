sleep 1;
curl -sLX POST 'https://dev.erpnext.host/api/method/returnable.returnable.doctype.returnable.returnable.install_returnables' \
-H 'Authorization: token db9bd25ee3f56ad:7c8ccc1f0c2f88e' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'company=Logichem Solutions S. A.' \
  | jq -r '.message.result';
