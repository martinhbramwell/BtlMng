echo -e "


<.............................................................................................>";

if [[ 1 -eq 0 ]]; then
    pushd ${TARGET_BENCH} >/dev/null;
    bench --site ${ERPNEXT_SITE_URL} execute returnable.hook_tasks.returnableMoveFromMaterialTransfer;
    popd >/dev/null;
else
    mysql -tAD _091b776d72ba8e16 < doIt.sql;
fi;

