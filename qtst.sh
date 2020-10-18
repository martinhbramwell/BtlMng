#!/usr/bin/env bash
#
export SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )";
export SCRIPT_NAME=$(basename "$0");

export QTST_DIR="/dev/shm/qtst";

mkdir -p ${QTST_DIR};

if [[ 0 == 1 ]]; then
cat << EOF > ${QTST_DIR}/qtst.py

row = ['Cust >> Stock', None, 'Envases Sucios - LSSA', 'IBAA324', 'RTN-BCH-00047059', 'RTN-BIT-000067195']

print('row')
print('Use to_stock' if row[0].split(' >> ')[0] == 'Stock' else 'Use to_customer')

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

# SELECT * FROM \`tabReturnable Holder\` ORDER BY name DESC LIMIT 20;

# SELECT "SHOW INDICES FROM \`tabReturnable\`, \`tabReturnable Batch\` AND \`tabReturnable Batch Item\`" \G
# SHOW INDEX FROM \`tabReturnable\`;
# SHOW INDEX FROM \`tabReturnable Batch\`;
# SHOW INDEX FROM \`tabReturnable Batch Item\`;

#     # SELECT DISTINCT  SQL_CALC_FOUND_ROWS
#     SELECT SQL_CALC_FOUND_ROWS
#         direction as Direccion
#       # , timestamp as creation
#       # , timestamp as modified
#       # , 'Administrator' as modified_by
#       # , 'Administrator' as owner
#       # , 0 as docstatus
#       # , I.bottle as parent
#       # , 'moves' as parentfield
#       # , 'Returnable' as parenttype
#       # , 1 as idx
#       , from_stock as "Del Almacén"
#       , from_customer as "Del Cliente"
#       , to_customer as "Al Cliente"
#       , to_stock as "Al Almacén"
#       , DATE(B.timestamp) as "Fecha"
#       , bapu_id as "ID BAPU"
#       # , IFNULL(from_customer, to_customer) as if_customer
#     FROM 
#         \`tabReturnable Batch\` B
#       , \`tabReturnable Batch Item\` I 
#     WHERE 
#         B.name = I.parent
#     AND I.bottle = "IBEE089"
#     ORDER BY I.bottle, timestamp
#     # LIMIT 4
#     ;

# SELECT FOUND_ROWS();
       # AND R.last_customer = '{0}'

    SELECT
        R.name as Retornable
      , DATE_FORMAT(B.timestamp, '%Y-%m-%d') as Desde
      FROM
          \`tabReturnable\` R
        , \`tabReturnable Batch\` B
        , \`tabReturnable Batch Item\` I
     WHERE
           I.bottle = R.name

       AND R.state IN ('Donde Cliente')
       AND B.to_customer = R.last_customer
       AND R.last_out = R.last_move
       AND I.parent = B.name
       AND B.direction NOT IN ('Cust >> Stock', 'Stock >> Stock')
       AND B.bapu_id in (
           SELECT
               MAX(M.timestamp)
             FROM
                 \`tabReturnable Batch\` M
               , \`tabReturnable Batch Item\` N
            WHERE N.parent = M.name
              AND M.to_customer IS NOT NULL
              AND M.to_customer = B.to_customer
              AND N.bottle = I.bottle
         GROUP BY M.to_customer, N.bottle
      )
    ORDER BY R.name
    ;

SELECT FOUND_ROWS();

    SELECT 
    FROM 
        \`tabReturnable Batch\` B
      , \`tabReturnable Batch Item\` I 
    WHERE 
        B.name = I.parent
    # AND I.bottle = "IBEE089"
    # ORDER BY I.bottle, timestamp
    LIMIT 1
    \G

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

cat << EOF > ${QTST_DIR}/qtst.sql
#     SELECT
#           I.bottle as Retornable
#         , DATE_FORMAT(B.timestamp, '%Y-%m-%d') as Desde
#         , B.to_customer as Cliente
#         , B.direction
#       FROM
#           \`tabReturnable Batch Item\` I
#         , \`tabReturnable Batch\` B
# --        , \`tabReturnable\` R
#      WHERE
#            I.bottle in ('IBDD881')
# --       AND I.bottle = R.name
# --       AND R.state IN ('Donde Cliente')
# --       AND B.to_customer = R.last_customer
# --       AND R.last_out = R.last_move
#        AND I.parent = B.name
#        AND B.direction NOT IN ('Cust >> Stock', 'Stock >> Stock')
#        AND B.timestamp in (
#            SELECT
#                MAX(M.timestamp)
#              FROM
#                  \`tabReturnable Batch\` M
#                , \`tabReturnable Batch Item\` N
#             WHERE N.parent = M.name
#               AND M.to_customer IS NOT NULL
#               AND M.to_customer = B.to_customer
#               AND N.bottle = I.bottle
#               AND I.bottle in ('IBDD881')
#          GROUP BY N.bottle
#       )
#     ORDER BY I.bottle
#     LIMIT 100
#     ;

# SET @bottle0 = 'IBCC586';
# SET @bottle0 = 'IBCC586';
# SET @bottle1 = 'IBDD636';
# SET @bottle1 = 'IBDD636';


# SET @bottle0 = 'IBDD644';
# SET @bottle1 = 'IBDD483';
# SET @bottle2 = 'IBAA133';
# SET @customer = 'Martha Castano Nicholls';

SET @bottle0 = 'IBEE002';
SET @bottle1 = '';
SET @bottle2 = '';
# SET @customer = 'Tamia Calapi';
SET @customer = 'EDWIN EFREN CEVALLOS ORTEGA';
SET @stock = '';
SET @sourceStock = 'Envases IB Llenos - LSSA';

# SET @bottle0 = 'IBCC423';
# SET @bottle1 = 'IBDD389';

UPDATE \`tabReturnable Batch\`
   SET to_stock = 'Envases IB Llenos - LSSA'
 WHERE to_stock = 'Envases Llenos - LSSA'
-- WHERE name = 'RTN-BCH-00047959'
-- WHERE timestamp > '2020-10-06 15:14:13'
;

#     # SELECT
#     #       I.name
#     #     , I.bottle
#     #     , C.Retornable
#     SELECT
#           B.name as Batch
#         , I.name
#         , B.timestamp
#         , C.fecha
#         , I.bottle
#         , C.Retornable
#         , B.bapu_id
#         , B.to_customer
#         , B.from_stock
#       FROM
#           \`tabReturnable Batch\` B
# INNER JOIN (
#            SELECT
#                  MAX(M.timestamp) as fecha
#                , N.bottle as Retornable
#              FROM
#                  \`tabReturnable Batch\` M
#                , \`tabReturnable Batch Item\` N
#             WHERE N.parent = M.name
#               AND M.to_customer IS NOT NULL
#          GROUP BY N.bottle
#       ) C ON C.fecha = B.timestamp
#          , \`tabReturnable Batch Item\` I

#       WHERE
#            I.parent = B.name
#        AND C.Retornable = I.bottle
#        AND I.bottle in (@bottle0, @bottle1, @bottle2)
#     ;

#     SELECT Retornable, MAX(Fecha)
#       FROM (
#            SELECT
#                  MAX(M.timestamp) as Fecha
#                , N.bottle as Retornable
#                , M.direction as Direccion
#              FROM
#                  \`tabReturnable Batch\` M
#                , \`tabReturnable Batch Item\` N
#             WHERE N.parent = M.name
#               AND N.bottle in (@bottle0, @bottle1, @bottle2)
#          GROUP BY Retornable, Direccion
#       ) A
#     GROUP BY Retornable
#     ;

#            SELECT
#               M.name, M.timestamp, N.name, N.bottle
#              FROM
#                  \`tabReturnable Batch\` M
#                , \`tabReturnable Batch Item\` N
#             WHERE N.parent = M.name
#               AND N.bottle in (@bottle0, @bottle1, @bottle2)
#               AND M.timestamp in ('2020-10-06 15:16:37.000000', '2020-09-30 13:48:02.000000', '2020-09-30 13:48:02.000000')


#           ;

#            SELECT
#                  N.bottle as Retornable
#                , M.direction as Direccion
#                , MAX(M.timestamp) as Fecha
# --               , M.to_customer as Customer
#              FROM
#                  \`tabReturnable Batch\` M
#                , \`tabReturnable Batch Item\` N
#             WHERE N.parent = M.name
# --              AND M.to_customer IS NOT NULL
# --              AND M.to_customer in ('Laura Montilla')
#               AND N.bottle in (@bottle0, @bottle1, @bottle2)
#          GROUP BY Retornable, Direccion
#          ORDER BY Retornable, Fecha
#       ;



    SELECT 'Tenencias del Cliente' \G

    SELECT SQL_CALC_FOUND_ROWS
          B.name          AS \`Lote\`
        , I.name          AS \`Item de Lote\`
        , B.timestamp     AS \`Fecha\`
--        , B.docstatus     AS \`Estado\`
        , C.Retornable    AS \`Retornable\`
        , B.bapu_id       AS \`ID_BAPU\`
--        , B.from_stock    AS \`Del Almacén\`
--        , B.from_customer AS \`Del Cliente\`
--        , B.to_customer   AS \`Al Cliente\`
--        , B.to_stock      AS \`Al Almacén\`
      FROM
          \`tabReturnable Batch\` B
INNER JOIN (
        SELECT Retornable, MAX(Fecha) AS Fecha
          FROM (
               SELECT
                     MAX(M.timestamp) AS Fecha
                   , N.bottle AS Retornable
                   , M.direction AS Direccion
                 FROM
                     \`tabReturnable Batch\` M
                   , \`tabReturnable Batch Item\` N
                WHERE N.parent = M.name
--                  AND N.bottle in (@bottle0, @bottle1, @bottle2)
                  AND M.docstatus = 1
             GROUP BY Retornable, Direccion
          ) A
        GROUP BY Retornable
      ) C ON C.Fecha = B.timestamp
         , \`tabReturnable Batch Item\` I
      WHERE
           I.parent = B.name
       AND C.Retornable = I.bottle
       AND B.docstatus = 1
       AND B.to_customer = @customer
--       AND I.bottle in (@bottle0, @bottle1, @bottle2)
    ;


SELECT FOUND_ROWS();


    SELECT '**********  Tenencias del Almacen  **********' \G

    SELECT
          C.Retornable      AS \`Retornable\`
        , DATE(B.timestamp) AS \`Desde\`
        , CONCAT("<a href='/desk#Form/Returnable%20Batch/", B.name, "' target='_blank'>", B.name,"</a>") as \`Lote\`
        , I.name            AS \`Item\`
        , B.bapu_id         AS \`IDBAPU\`
      FROM
          \`tabReturnable Batch\` B
INNER JOIN (
        SELECT Retornable, MAX(Fecha) AS Fecha
          FROM (
               SELECT
                     MAX(M.timestamp) AS Fecha
                   , N.bottle AS Retornable
                   , M.direction AS Direccion
                 FROM
                     \`tabReturnable Batch\` M
                   , \`tabReturnable Batch Item\` N
                WHERE N.parent = M.name
                  AND M.docstatus = 1
             GROUP BY Retornable, Direccion
          ) A
        GROUP BY Retornable
      ) C ON C.Fecha = B.timestamp
         , \`tabReturnable Batch Item\` I
     WHERE
           B.to_stock = @sourceStock
       AND I.parent = B.name
       AND C.Retornable = I.bottle
       AND B.docstatus = 1
  ORDER BY Retornable
;

# SELECT FOUND_ROWS();

# select distinct to_stock from \`tabReturnable Batch\` B;
# select distinct from_stock from \`tabReturnable Batch\` B;
# select * from \`tabWarehouse\` W;

# select * from \`tabReturnable Movement\` B LIMIT 2;
# select * from \`tabReturnable\` B where ;




#      SELECT
#           M.name
#         , N.name
#         , N.bottle
#         , M.timestamp
#         , M.docstatus
#         , bapu_id
#         , direction as Direccion
#         , from_stock as "Del Almacén"
#         , from_customer as "Del Cliente"
#         , to_customer as "Al Cliente"
#         , to_stock as "Al Almacén"

#        FROM
#            \`tabReturnable Batch\` M
#          , \`tabReturnable Batch Item\` N
#       WHERE N.parent = M.name
#         AND M.name in ('RTN-BCH-00047959')
# --        AND M.name in ('RTN-BCH-00014877')
# --        AND N.name in ('RTN-BIT-000087407', 'RTN-BIT-000077703', 'RTN-BIT-000073752')
#       ORDER BY N.bottle desc
#     ;



#            I.bottle in ('IBDD881')
# --       AND I.bottle = R.name
# --       AND R.state IN ('Donde Cliente')
# --       AND B.to_customer = R.last_customer
# --       AND R.last_out = R.last_move
#        AND I.parent = B.name
#        AND B.direction NOT IN ('Cust >> Stock', 'Stock >> Stock')
#        AND B.timestamp in (
#            SELECT
#                MAX(M.timestamp)
#              FROM
#                  \`tabReturnable Batch\` M
#                , \`tabReturnable Batch Item\` N
#             WHERE N.parent = M.name
#               AND M.to_customer IS NOT NULL
#               AND M.to_customer = B.to_customer
#               AND N.bottle = I.bottle
#               AND I.bottle in ('IBDD881')
#          GROUP BY N.bottle
#       )
#     ORDER BY I.bottle
#     LIMIT 100
#     ;

    # SELECT
    #     B.name
    #   , B.timestamp
    #   , B.bapu_id
    #   FROM
    #       \`tabReturnable Batch\` B
    #     , \`tabReturnable Batch Item\` I
    #  WHERE
    #        I.parent = B.name
    #    AND B.direction NOT IN ('Cust >> Stock', 'Stock >> Stock')
    #    AND IFNULL(B.to_customer, B.from_customer) = 'Acrimecsa del Ecuador S.A'
    # # LIMIT 5
    # ;
    # #    AND R.state IN ('Donde Cliente')
    # #    AND B.to_customer = R.last_customer
    # #    AND R.last_out = R.last_move
    # #    AND I.parent = B.name
    # #    AND B.direction NOT IN ('Cust >> Stock', 'Stock >> Stock')
    # #    AND B.bapu_id in (
    # #        SELECT
    # #            MAX(M.timestamp)
    # #          # , B.to_customer
    # #          # , I.bottle
    # #          FROM
    # #              \`tabReturnable Batch\` M
    # #            , \`tabReturnable Batch Item\` N
    # #         WHERE N.parent = M.name
    # #           AND M.to_customer IS NOT NULL
    # #           AND M.to_customer = B.to_customer
    # #           AND N.bottle = I.bottle
    # #      GROUP BY M.to_customer, N.bottle
    # #   )
    # ORDER BY B.timestamp
;


     SELECT
           B.direction     as \`Direccion\`
         , B.to_customer   as \`Al Cliente\`
         , B.to_stock      as \`Al Almacén\`
         , B.from_customer as \`Del Cliente\`
         , B.from_stock    as \`Del Almacén\`
         , C.Retornable    as \`Retornable\`
         , B.name          as \`Lote\`
         , I.name          as \`Item\`
         , B.timestamp     as \`Fecha\`
         , B.docstatus     as \`Estado\`
         , B.bapu_id       as \`ID_BAPU\`
       FROM
           \`tabReturnable Batch\` B
 INNER JOIN (
         SELECT Retornable, MAX(Fecha) as Fecha
           FROM (
                SELECT
                      MAX(M.timestamp) as Fecha
                    , N.bottle as Retornable
                    , M.direction as Direccion
                  FROM
                      \`tabReturnable Batch\` M
                    , \`tabReturnable Batch Item\` N
                 WHERE N.parent = M.name
                   AND N.bottle in ("IBDD505")
                   AND M.docstatus = 1
              GROUP BY Retornable, Direccion
           ) A
         GROUP BY Retornable
       ) C ON C.Fecha = B.timestamp
          , \`tabReturnable Batch Item\` I
       WHERE
            I.parent = B.name
        AND C.Retornable = I.bottle
        AND B.docstatus = 1
        AND I.bottle in ("IBDD505")
;


EOF
    # SELECT
    #     R.name as Retornable
    #   , DATE_FORMAT(B.timestamp, '%Y-%m-%d') as Desde
    #   FROM
    #       \`tabReturnable\` R
    #     , \`tabReturnable Batch\` B
    #     , \`tabReturnable Batch Item\` I
    #  WHERE
    #        I.bottle = R.name

    #    AND R.state IN ('Donde Cliente')
    #    AND B.to_customer = R.last_customer
    #    AND R.last_out = R.last_move
    #    AND I.parent = B.name
    #    AND B.direction NOT IN ('Cust >> Stock', 'Stock >> Stock')
    #    AND B.bapu_id in (
    #        SELECT
    #            MAX(M.timestamp)
    #          FROM
    #              \`tabReturnable Batch\` M
    #            , \`tabReturnable Batch Item\` N
    #         WHERE N.parent = M.name
    #           AND M.to_customer IS NOT NULL
    #           AND M.to_customer = B.to_customer
    #           AND N.bottle = I.bottle
    #      GROUP BY M.to_customer, N.bottle
    #   )
    # ORDER BY R.name
    # ;
cat << QTEOF > ${QTST_DIR}/qtst.sql

    # SELECT 'Loading \`tabRetBat\` from \`/opt/ErpNext_DocTypeHandlers/docType_Returnable_Batch.csv\`' \G

    # DROP TABLE IF EXISTS \`tabRetBat\`;
    # CREATE TABLE IF NOT EXISTS \`tabRetBat\` SELECT * FROM \`tabReturnable Batch\` LIMIT 1;

    # DELETE FROM \`tabRetBat\`;

    # LOAD DATA LOCAL INFILE
    # '/opt/ErpNext_DocTypeHandlers/docType_Returnable_Batch.csv'
    #   INTO TABLE \`tabRetBat\`
    #   FIELDS TERMINATED BY ',' ENCLOSED BY '\"'
    #   IGNORE 1 LINES
    #   (name, creation, modified, timestamp, modified_by, owner, direction, from_stock, to_customer, from_customer, to_stock, bapu_id, returnables)
    # ;

    # SET @idx := 0;
    # UPDATE \`tabRetBat\` SET amended_from = CONCAT('RTN-BCH-', LPAD(  ( SELECT @idx := @idx + 1 ), 8, '0')) ORDER BY timestamp;
    # UPDATE \`tabRetBat\` SET name = CONCAT('X', name);

    # SELECT * FROM \`tabRetBat\` WHERE amended_from > 'RTN-BCH-00048254' ORDER BY name;

    # ALTER TABLE \`tabRetBat\` ADD INDEX \`amended_from_index\` (\`amended_from\`);
    # ALTER TABLE \`tabRetBat\` ADD INDEX \`bapu_id_index\` (\`bapu_id\`);
    # ALTER TABLE \`tabRetBat\` ADD PRIMARY KEY(name);

    # # SHOW CREATE TABLE \`tabRetBat\`;
    # # DESCRIBE \`tabRetBat\`;


    # SELECT 'Loading \`tabRetBatItm\` from \`/opt/ErpNext_DocTypeHandlers/docType_Returnable_Batch_Item.csv\`' \G

    # DROP TABLE IF EXISTS \`tabRetBatItm\`;
    # CREATE TABLE IF NOT EXISTS \`tabRetBatItm\` SELECT * FROM \`tabReturnable Batch Item\` LIMIT 1;

    # DELETE FROM \`tabRetBatItm\`;

    # LOAD DATA LOCAL INFILE
    # '/opt/ErpNext_DocTypeHandlers/docType_Returnable_Batch_Item.csv'
    #   INTO TABLE \`tabRetBatItm\`
    #   FIELDS TERMINATED BY ',' ENCLOSED BY '\"'
    #   IGNORE 1 LINES
    #   (name, creation, modified, modified_by, owner, parent, parentfield, parenttype, idx, bottle)
    # ;

    # UPDATE \`tabRetBatItm\` SET parent = CONCAT('X', parent);

    # ALTER TABLE \`tabRetBatItm\` ADD INDEX \`parent_index\` (\`parent\`);
    # ALTER TABLE \`tabRetBatItm\` ADD PRIMARY KEY(name);


    # SELECT 'Getting new primary key of \`tabRetBat\` to be parent of  \`tabRetBatItm\`' \G

    # UPDATE \`tabRetBatItm\` I JOIN \`tabRetBat\` B ON I.parent = B.name
    # SET I.amended_from = B.amended_from;

    # ALTER TABLE \`tabRetBatItm\` ADD INDEX \`amended_from_index\` (\`amended_from\`);

    # SELECT 'Setting new primary key of \`tabRetBat\` and  \`tabRetBatItm\`' \G

    # UPDATE \`tabRetBat\` B SET B.name = B.amended_from;
    # UPDATE \`tabRetBat\` B SET B.amended_from = NULL;
    # UPDATE \`tabRetBatItm\` I SET I.parent = I.amended_from;
    # UPDATE \`tabRetBatItm\` I SET I.amended_from = NULL;


    # SELECT 'Getting new primary key of \`tabRetBatItm\`' \G
    # SET @idx := 0;
    # UPDATE \`tabRetBatItm\` SET amended_from = CONCAT('RTN-BIT-', LPAD(  ( SELECT @idx := @idx + 1 ), 8, '0')) ORDER BY parent, idx;
    # UPDATE \`tabRetBatItm\` SET name = CONCAT('X', name);

    # SELECT 'Setting new primary key of \`tabRetBatItm\`' \G
    # UPDATE \`tabRetBatItm\` I SET I.name = I.amended_from;
    # UPDATE \`tabRetBatItm\` I SET I.amended_from = NULL;

    # # SELECT * FROM \`tabRetBat\` B LIMIT 5;
    # # SELECT * FROM \`tabRetBatItm\` I LIMIT 5;

    # # SELECT B.creation, B.name, I.name, B.timestamp, I.idx, I.bottle, B.bapu_id
    # #   FROM \`tabRetBat\` B 
    # #   JOIN \`tabRetBatItm\` I 
    # #     ON B.name = I.parent 
    # #  WHERE I.idx > 2
    # #    AND B.timestamp > '2020-10-01'
    # #    ORDER BY B.name, I.name
    # # LIMIT 50;


    # # SELECT B.creation, B.name, I.name, B.timestamp, I.idx, I.bottle, B.bapu_id
    # #   FROM \`tabRetBat\` B 
    # #   JOIN \`tabRetBatItm\` I 
    # #     ON B.name = I.parent 
    # #  WHERE B.bapu_id = 'E_0014850'
    # #    ORDER BY B.name, I.name
    # # LIMIT 50;

    # # # DESCRIBE \`tabRetBatItm\`;


QTEOF

cat << SREOF > ${QTST_DIR}/qtst.sql


SET @CUSTOMER := "Avix%";

    SELECT SQL_CALC_FOUND_ROWS
          C.Retornable      AS \`Retornable\`
        , DATE(B.timestamp) AS \`Desde\`
        , CONCAT("<a href='/desk#Form/Returnable%20Batch/", B.name, "' target='_blank'>", B.name,"</a>") as \`Lote\`
        , I.name            AS \`Item\`
        , B.docstatus       AS \`Status\`
        , I.docstatus       AS \`Item Status\`
        , B.bapu_id         AS \`IDBAPU\`
        , B.to_customer     AS \`Customer\`
      FROM
          \`tabReturnable Batch\` B
INNER JOIN (
        SELECT Retornable, MAX(Fecha) AS Fecha
          FROM (
               SELECT
                     MAX(M.timestamp) AS Fecha
                   , N.bottle AS Retornable
                   , M.direction AS Direccion
                 FROM
                     \`tabReturnable Batch\` M
                   , \`tabReturnable Batch Item\` N
                WHERE N.parent = M.name
--                  AND M.docstatus = 1
             GROUP BY Retornable, Direccion
          ) A
        GROUP BY Retornable
      ) C ON C.Fecha = B.timestamp
         , \`tabReturnable Batch Item\` I
      WHERE
           I.parent = B.name
       AND C.Retornable = I.bottle
--       AND B.docstatus = 1
       AND B.to_customer like @CUSTOMER
  ORDER BY B.timestamp DESC
;

# UPDATE \`tabReturnable Batch\` M SET M.docstatus = 1;
# UPDATE \`tabReturnable Batch Item\` N SET N.docstatus = 1;

SELECT MAX(B.name) from \`tabReturnable Batch\` B;
SELECT MAX(I.name) from \`tabReturnable Batch Item\` I;

#         SELECT Retornable, MAX(Fecha) AS Fecha
#           FROM (
#                SELECT
#                      MAX(M.timestamp) AS Fecha
#                    , N.bottle AS Retornable
#                    , M.direction AS Direccion
#                  FROM
#                      \`tabReturnable Batch\` M
#                    , \`tabReturnable Batch Item\` N
#                 WHERE N.parent = M.name
# --                  AND M.docstatus = 1
#              GROUP BY Retornable, Direccion
#           ) A
#         GROUP BY Retornable
# ;


SREOF


mysql -t ${1} < ${QTST_DIR}/qtst.sql;
fi;


# 


echo -e "\n/* ~~~~~~~~~ Curtailed ~~~~~~~ ${SCRIPT_NAME} ~~~~~~~~ */";
exit;
