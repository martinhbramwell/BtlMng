#!/usr/bin/env bash
#
export SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )";
export SCRIPT_NAME=$(basename "$0");

export QTST_DIR="/dev/shm/qtst";

mkdir -p ${QTST_DIR};

if [[ 1 == 1 ]]; then
cat << EOF > ${QTST_DIR}/qtst.py

# query_result = [
#   { "xAxisField":  30, "yAxisField": 4156.78 },
#   { "xAxisField":  45, "yAxisField": 3908.34 },
#   { "xAxisField":  60, "yAxisField": 5632.87 },
#   { "xAxisField":  75, "yAxisField": 5698.21 },
#   { "xAxisField":  90, "yAxisField": 2321.54 },
#   { "xAxisField": 105, "yAxisField": 4446.88 }
# ]
# # print(query_result)

# columns = [
#     {
#       "fieldname": "xAxisField",
#       "fieldtype": "Int",
#       "label": "X-Axis",
#       "width": 100
#     },
#     {
#       "fieldname": "yAxisField",
#       "fieldtype": "Currency",
#       "label": "Y-Axis",
#       "width": 100
#     },
#   ]

# attributes = [d.get("fieldname") for d in columns]
# # print('attributes')
# # print(attributes)

# dimensions = [
#   [ value.get(attr) for value in query_result ] for attr in attributes
# ]

# labels = dimensions[0];
# values = dimensions[1];
# print(labels)

def recoverDate(date):
  return str(date).upper()


rslt = (('Ines Checa', 'datetime.date(2016, 1, 1)', 'IBCC315', 'Stock >> Cust', 'Donde Cliente'), ('Ines Checa', 'datetime.date(2016, 1, 1)', 'IBCC328', 'Stock >> Cust', 'Donde Cliente'))
print(rslt)

table = [list(row) for row in rslt]
for row in table:
  row[1] = str(row[1]).upper()

table = [[str(col) for col in row] for row in rslt]

print('table')
print(table)

EOF

# ython3 ${QTST_DIR}/qtst.py;
python3 ${QTST_DIR}/qtst.py > chart.json;

cat chart.json;
# sed -i "s/'/\"/g" chart.json;

# cat chart.json;

# jq -r '.' chart.json;


else


   # SELECT last_customer AS "Last Customer", state AS "Current State", count(*) as qty, IFNULL(M.to_customer, M.to_stock) AS "Last Location"
cat << EOF > ${QTST_DIR}/qtst.sql
--   SELECT *
   SELECT IFNULL(from_customer, to_customer) AS Cliente, DATE(M.timestamp) AS Fecha, R.name AS Retornable, M.direction AS 'Dirección', R.state AS Estado
     FROM \`tabReturnable\` R
LEFT JOIN \`tabReturnable Movement\` M
       ON R.name = M.parent
      AND IFNULL(to_customer, from_customer) = 'Ines Checa'
    WHERE R.state NOT IN ('Confuso')
      AND M.direction NOT IN ('Stock >> Stock')
      AND M.direction IS NOT NULL
 ORDER BY IFNULL(to_customer, from_customer), timestamp, direction
EOF
    # LIMIT 2 \G
# --      AND R.last_customer = M.to_customer
#       AND R.last_move = M.idx
#    HAVING qty > 5
#  ORDER BY last_customer, state


# cat << EOF > ${QTST_DIR}/qtst.sql
# SELECT parent FROM \`tabDesk Card\`;
# SELECT name. tax_id FROM \`tabCustomer\` WHERE name = 'Tito Banda' \G
# EOF


# cat << EOF > ${QTST_DIR}/qtst.sql
# SELECT code FROM \`tabReturnable\` where state = 'Lleno' and code in ('CLAA191', 'IBCC634') LIMIT 5;     -- \G;
# SELECT code FROM \`tabReturnable\` where state = 'Lleno' LIMIT 5;     -- \G;
# SELECT * FROM \`tabReturnable Batch Item\` LIMIT 5;     -- \G;
# EOF

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
