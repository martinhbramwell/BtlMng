#!/usr/bin/env bash
#
export SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )";
export SCRIPT_NAME=$(basename "$0");

export QTST_DIR="/dev/shm/qtst";

mkdir -p ${QTST_DIR};

if [[ 1 == 1 ]]; then
cat << EOF > ${QTST_DIR}/qtst.py

query_result = [
  { "xAxisField":  30, "yAxisField": 4156.78 },
  { "xAxisField":  45, "yAxisField": 3908.34 },
  { "xAxisField":  60, "yAxisField": 5632.87 },
  { "xAxisField":  75, "yAxisField": 5698.21 },
  { "xAxisField":  90, "yAxisField": 2321.54 },
  { "xAxisField": 105, "yAxisField": 4446.88 }
]
# print(query_result)

columns = [
    {
      "fieldname": "xAxisField",
      "fieldtype": "Int",
      "label": "X-Axis",
      "width": 100
    },
    {
      "fieldname": "yAxisField",
      "fieldtype": "Currency",
      "label": "Y-Axis",
      "width": 100
    },
  ]

attributes = [d.get("fieldname") for d in columns]
# print('attributes')
# print(attributes)

dimensions = [
  [ value.get(attr) for value in query_result ] for attr in attributes
]

labels = dimensions[0];
values = dimensions[1];
print(labels)
print(values)


EOF

# ython3 ${QTST_DIR}/qtst.py;
python3 ${QTST_DIR}/qtst.py > chart.json;

cat chart.json;
# sed -i "s/'/\"/g" chart.json;

# cat chart.json;

# jq -r '.' chart.json;


else

# cat << EOF > ${QTST_DIR}/qtst.sql
# SELECT code FROM \`tabReturnable\` where state = 'Lleno' and code in ('CLAA191', 'IBCC634') LIMIT 5;     -- \G;
# SELECT code FROM \`tabReturnable\` where state = 'Lleno' LIMIT 5;     -- \G;
# SELECT * FROM \`tabReturnable Batch Item\` LIMIT 5;     -- \G;
# EOF

cat << EOF > ${QTST_DIR}/qtst.sql
# SELECT distinct parent FROM \`tabReturnable Batch\` WHERE parent IS NOT NULL;
# SELECT * FROM \`tabReturnable Batch\` WHERE (to_customer = 'Andres Karolys' OR from_customer = 'Andres Karolys') order by timestamp LIMIT 15;     -- \G;
SELECT DISTINCT IFNULL(to_customer, from_customer) as name FROM \`tabReturnable Movement\` LIMIT 15;     -- \G;
# SELECT * FROM \`tabReturnable Movement\` WHERE to_customer = 'Jose Cordova' OR from_customer = 'Jose Cordova' order by timestamp LIMIT 15;     -- \G;
# SELECT * FROM \`tabReturnable Batch Item\` WHERE parent = 'RTN-BCH-000000007'  LIMIT 5;     -- \G;

SELECT C.name FROM \`tabCustomer\` C WHERE C.name NOT IN (SELECT DISTINCT IFNULL(to_customer, from_customer) as name FROM \`tabReturnable Movement\` ) LIMIT 100;     -- \G;
SELECT C.name FROM \`tabCustomer\` C WHERE C.name = 'Veggie';


EOF

# cat << EOF > ${QTST_DIR}/qtst.sql
# SELECT * FROM \`tabCustomer\` WHERE name like 'Andres Ka%' LIMIT 5;     -- \G;
# EOF

# cat << EOF > ${QTST_DIR}/qtst.sql
#    SELECT last_customer AS "Last Customer", state AS "Current State", count(*) as qty, IFNULL(M.to_customer, M.to_stock) AS "Last Location"
#      FROM \`tabReturnable\` R
# LEFT JOIN \`tabReturnable Movement\` M
#        ON R.name = M.parent
# --      AND R.last_customer = M.to_customer
#       AND R.last_move = M.idx
#  GROUP BY last_customer, state
#    HAVING qty > 5
#  ORDER BY last_customer, state
#     LIMIT 100;

#    SELECT last_customer AS "Last Customer", state AS "Current State", count(*) as qty, S.customer
#      FROM \`tabReturnable\` R
# LEFT JOIN (SELECT M.parent, M.to_customer as customer, MAX(idx) AS last_out FROM \`tabReturnable Movement\` M GROUP BY M.parent) S
#        ON R.name = S.parent AND R.last_out = S.last_out
#     WHERE last_customer IN ('LOGICHEM SOLUTIONS S.A', 'Iridium Blue (Venta No Registrada)', 'ALERTAR', 'Iridium Blue Agua', '', 'Daniel Leonardo Wild Stapel', 'Envases Rotos')
#  GROUP BY last_customer, state
# --   HAVING qty > 5
# -- ORDER BY qty desc
# ;

# -- ORDER BY last_customer, state
# --    LIMIT 100;

# SELECT parent, MAX(idx) FROM \`tabReturnable Movement\` GROUP BY parent LIMIT 4;
# EOF

#    SELECT last_customer AS "Last Customer", state AS "Current State", count(*) as qty
#      FROM \`tabReturnable\` R
# --    WHERE last_customer IN ('LOGICHEM SOLUTIONS S.A', 'Iridium Blue (Venta No Registrada)', 'ALERTAR', 'Iridium Blue Agua', '', 'Envases Rotos')
#  GROUP BY last_customer, state
# --   HAVING qty > 1
#  ORDER BY state, last_customer, qty desc
#  ;

# cat << EOF > ${QTST_DIR}/qtst.sql

# --   SELECT last_customer AS "Last Customer", state AS "Current State", count(*) as qty, IFNULL(M.to_customer, M.to_stock) AS "Last Location"
#    SELECT *
#      FROM \`tabReturnable\` R
#      JOIN \`tabReturnable Movement\` M
#        ON R.name = M.parent
#       AND R.last_customer = 'Cerveceria SABAIBEER S.A.'
#       AND R.last_customer = M.to_customer
#       AND R.last_move = M.idx
#       AND M.timestamp > '2019-09-01'
#     LIMIT 10;

# SELECT * FROM \`tabReturnable Movement\` where to_customer = 'Super Foods Ecuador Cia Ltda' and creation > '2020-09-01' LIMIT 50;
# SELECT * FROM \`tabReturnable Batch\` where to_customer = 'Super Foods Ecuador Cia Ltda' and creation > '2020-09-10' LIMIT 50; --  and creation > '2019-01-01' LIMIT 5;



# EOF
# SELECT * FROM \`tabReturnable\` LIMIT 4;

echo -e "
";

mysql -t ${1} < ${QTST_DIR}/qtst.sql;
fi;

echo -e "\n\n/* ~~~~~~~~~ Curtailed ~~~~~~~ ${SCRIPT_NAME} ~~~~~~~~ */
";
exit;
