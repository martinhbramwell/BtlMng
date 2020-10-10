#!/usr/bin/env bash
#
export SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )";
export SCRIPT_NAME=$(basename "$0");

export QTST_DIR="/dev/shm/qtst";

mkdir -p ${QTST_DIR};

if [[ 1 == 0 ]]; then
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


cat << EOF > ${QTST_DIR}/qtst.sql

    # SELECT 'Loading temporary table \`RTN_HLD\` from \`tabReturnable\`, \`tabReturnable Batch\` and \`tabReturnable Batch Item\`' \G

    # DROP TABLE IF EXISTS \`RTN_HLD\`;

    # CREATE TABLE \`RTN_HLD\`
    #   (name INT AUTO_INCREMENT PRIMARY KEY)
    # AS


    # SELECT
    #   *
    # FROM
    #     \`tabReturnable\` R
    # # WHERE
    # #       B.timestamp > '2020-09-18 13:03:29.000000'
    # ORDER BY R.bapu_id asc
    # LIMIT 5;

    # SELECT
    #     I.parent
    #   , I.name
    #   , I.idx
    #   , I.bottle
    #   , I.creation
    # FROM
    #     \`tabReturnable Batch Item\` I
    # WHERE I.creation > '2020-10-06 15:15:58.000000'
    # ORDER BY I.creation desc
    # # LIMIT 15
    # ;


    # SELECT
    #     R.name
    #   , R.last_customer
    #   , R.state
    #   , R.last_out
    #   , R.last_move
    # FROM
    #     \`tabReturnable\` R
    # LIMIT 5
    # ;


    # SELECT
    #     *
    # SELECT
    # SELECT SQL_CALC_FOUND_ROWS
    #     *

# keep  # SELECT SQL_CALC_FOUND_ROWS
#       #     B.timestamp as creation
#       #   , B.timestamp as modified
#       #   , 'Administrator' as modified_by
#       #   , 'Administrator' as owner
#       #   , 0 as docstatus
#       #   , R.last_customer as parent
#       #   , 'retornables' as parentfield
#       #   , 'Customer' as parenttype
#       #   , 1 as idx
#       #   , R.name as returnable
#       # FROM
#       #     \`tabReturnable\` R
#       #   , \`tabReturnable Batch\` B
#       #   , \`tabReturnable Batch Item\` I
#       # WHERE
#       #       I.bottle = R.name
#       #   AND R.state IN ('Donde Cliente')
#       #   AND B.to_customer = R.last_customer
#       #   AND R.last_customer NOT IN ('Envases Rotos', 'ALERTAR')
#       #   AND R.last_out = R.last_move
#       #   AND I.parent = B.name
#       #   AND B.direction NOT IN ('Cust >> Stock', 'Stock >> Stock')
#       #   AND B.bapu_id in (
#       #        SELECT
#       #            MAX(M.bapu_id)
#       #          # , B.to_customer
#       #          # , I.bottle
#       #        FROM
#       #            \`tabReturnable Batch\` M
#       #          , \`tabReturnable Batch Item\` N
#       #        WHERE N.parent = M.name
#       #          AND M.to_customer IS NOT NULL
#       #          AND M.to_customer = B.to_customer
#       #          AND N.bottle = I.bottle
#       #     GROUP BY M.to_customer, N.bottle
#       #   )
#       # #   AND R.name in ('IBDD290', 'IBDD911', 'IBDD267', 'IBDD742', 'IBDD146', 'IBAA967', 'IBDD254', 'IBCC210', 'IBAA025', 'IBAA415', 'IBDD862', 'IBDD655', 'IBDD615', 'IBDD563', 'IBCC296', 'IBAA553', 'IBCC331', 'IBAA522', 'IBCC916', 'IBDD661')
#       # # GROUP BY R.name
#       # # HAVING cnt > 2
#       # ORDER BY R.last_customer, I.bottle, B.creation desc
#       # # LIMIT 8
#       # ;
#       # ;
#       # SELECT FOUND_ROWS();
# keep  # ;

SELECT * FROM \`tabReturnable Holder\` ORDER BY name DESC LIMIT 20;

SELECT "SHOW INDICES FROM \`tabReturnable\`, \`tabReturnable Batch\` AND \`tabReturnable Batch Item\`" \G
SHOW INDEX FROM \`tabReturnable\`;
SHOW INDEX FROM \`tabReturnable Batch\`;
SHOW INDEX FROM \`tabReturnable Batch Item\`;

    # SELECT DISTINCT  SQL_CALC_FOUND_ROWS
    SELECT SQL_CALC_FOUND_ROWS
        direction as Direccion
      # , timestamp as creation
      # , timestamp as modified
      # , 'Administrator' as modified_by
      # , 'Administrator' as owner
      # , 0 as docstatus
      # , I.bottle as parent
      # , 'moves' as parentfield
      # , 'Returnable' as parenttype
      # , 1 as idx
      , from_stock as "Del Almacén"
      , from_customer as "Del Cliente"
      , to_customer as "Al Cliente"
      , to_stock as "Al Almacén"
      , DATE(B.timestamp) as "Fecha"
      , bapu_id as "ID BAPU"
      # , IFNULL(from_customer, to_customer) as if_customer
    FROM 
        \`tabReturnable Batch\` B
      , \`tabReturnable Batch Item\` I 
    WHERE 
        B.name = I.parent
    AND I.bottle = "IBEE089"
    ORDER BY I.bottle, timestamp
    # LIMIT 4
    ;

SELECT FOUND_ROWS();

# describe \`tabReturnable Batch\`;
    
    # LIMIT 5
    # ;
         # AND I.bottle in ('IBDD290', 'IBDD911', 'IBDD267', 'IBDD742', 'IBDD146', 'IBAA967', 'IBDD254', 'IBCC210', 'IBAA025', 'IBAA415', 'IBDD862', 'IBDD655', 'IBDD615', 'IBDD563', 'IBCC296', 'IBAA553', 'IBCC331', 'IBAA522', 'IBCC916', 'IBDD661')


    # SELECT * FROM \`RTN_HLD\` ORDER BY name DESC LIMIT 10;


    # SELECT 'Loading temporary table \`RTN_HLD\` from \`tabReturnable\`, \`tabReturnable Batch\` and \`tabReturnable Batch Item\`' \G

    # DROP TABLE IF EXISTS \`RTN_HLD\`;

    # CREATE TABLE \`RTN_HLD\`
    #   (name INT AUTO_INCREMENT PRIMARY KEY)
    # AS
    # SELECT DISTINCT
    #     B.timestamp as creation
    #   , B.timestamp as modified
    #   , 'Administrator' as modified_by
    #   , 'Administrator' as owner
    #   , 0 as docstatus
    #   , R.last_customer as parent
    #   , 'retornables' as parentfield
    #   , 'Customer' as parenttype
    #   , 1 as idx
    #   , R.name as returnable
    # FROM
    #     \`tabReturnable\` R
    #   , \`tabReturnable Batch\` B
    #   , \`tabReturnable Batch Item\` I
    # WHERE
    #       B.to_customer = R.last_customer
    #   AND I.bottle = R.code
    #   AND I.idx = R.last_out
    #   AND I.parent = B.name
    #   AND R.state = 'Donde Cliente'
    # ORDER BY R.last_customer
    # ;

    # SELECT * FROM \`RTN_HLD\` ORDER BY name DESC LIMIT 10;


    # SELECT 'Loading \`tabReturnable Holder\` from \`temporary table\`' \G

    # DELETE
    # FROM \`tabReturnable Holder\`
    # ;

    # INSERT INTO \`tabReturnable Holder\` (
    #     name
    #   , creation
    #   , modified
    #   , modified_by
    #   , owner
    #   , docstatus
    #   , parent
    #   , parentfield
    #   , parenttype
    #   , idx
    #   , returnable
    # )
    # SELECT
    #     CONCAT('RTN-CST-', LPAD(name, 8, "0")) AS name
    #   , creation
    #   , modified
    #   , modified_by
    #   , owner
    #   , docstatus
    #   , parent
    #   , parentfield
    #   , parenttype
    #   , idx
    #   , returnable
    # FROM \`RTN_HLD\`
    # ;

    # SELECT * FROM \`tabReturnable Holder\` ORDER BY name DESC LIMIT 20;


    # SELECT 'Resetting \`tabReturnable Holder\` row indexes' \G;

    # UPDATE \`tabReturnable Holder\` TH,
    #   (
    #     SELECT
    #       @idx := IF(@returnable = parent, @idx + 1, 1) idx,
    #       @returnable := parent parent,
    #       name
    #     FROM
    #       (SELECT @returnable := NULL, @idx := 1) vars
    #       JOIN \`tabReturnable Holder\`
    #     ORDER BY
    #       parent, name
    #   ) XX
    # SET TH.idx=XX.idx WHERE TH.name=XX.name
    # ;

    # SELECT * FROM \`tabReturnable Holder\` ORDER BY name DESC LIMIT 10;

EOF

# cat << EOF > ${QTST_DIR}/qtst.sql
#    SELECT IFNULL(from_customer, to_customer) AS Cliente, DATE(M.timestamp) AS Fecha, R.name AS Retornable, M.direction AS 'Dirección', R.state AS Estado
#      FROM \`tabReturnable\` R
# LEFT JOIN \`tabReturnable Movement\` M
#        ON R.name = M.parent
#       AND IFNULL(to_customer, from_customer) = 'Ines Checa'
#     WHERE R.state NOT IN ('Confuso')
#       AND M.direction NOT IN ('Stock >> Stock')
#       AND M.direction IS NOT NULL
#  ORDER BY IFNULL(to_customer, from_customer), timestamp, direction
# EOF
#     # LIMIT 2 \G


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

# cat << EOF > ${QTST_DIR}/qtst.sql

# EOF

mysql -t ${1} < ${QTST_DIR}/qtst.sql;
fi;

echo -e "\n/* ~~~~~~~~~ Curtailed ~~~~~~~ ${SCRIPT_NAME} ~~~~~~~~ */";
exit;
