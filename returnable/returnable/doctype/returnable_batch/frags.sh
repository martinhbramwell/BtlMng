source ../../../../envars.sh
echo -e "Database: ${ERPNEXT_SITE_DB}";
mysql -A ${ERPNEXT_SITE_DB} < ./frags.sql
