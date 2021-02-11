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
          B.name          AS \`Lote\`"
        , "I.name          AS \`Item de Lote\`
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
        , CONCAT("<a href='/desk#Form/Returnable%20Batch/", B.name, "' target='_blank'>", B.name,"</a>") as \`Lote\`"
        , "I.name            AS \`Item\`
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
        , CONCAT("<a href='/desk#Form/Returnable%20Batch/", B.name, "' target='_blank'>", B.name,"</a>") as \`Lote\`"
        , "I.name            AS \`Item\`
        , B.docstatus       AS \`Status\`"
        , "I.docstatus       AS \`Item Status\`
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

# SHOW CREATE TABLE \`tabReturnable\`;
SELECT
    name
  , docstatus
  , parent
  , idx
  , naming_series
  , code
  , state
  , times_out
  , times_in
  , id
  , last_customer
  , bapu_id
  , fills
  , last_out
  , last_move
  FROM \`tabReturnable\`
 LIMIT 1
 \G

  SELECT
      name
    , docstatus
    , parent
    , idx
    , naming_series
    , code
    , state
    , times_out
    , times_in
    , id
    , last_customer
    , bapu_id
    , fills
    , last_out
    , last_move
  FROM \`tabReturnable\`
ORDER BY name DESC
 LIMIT 5
;
SELECT 'Showed \`tabReturnable\`\n\n\n' as \`Comment\` \G;

SELECT
    name
  , docstatus
  , parent
  , idx
  , bottle
  , direction
  , from_stock
  , from_customer
  , to_customer
  , to_stock
  , timestamp
  , bapu_id
  , if_customer
  FROM \`tabReturnable Movement\`
 LIMIT 1
 \G

  SELECT
        name
      , docstatus
      , parent
      , idx
      , bottle
      , direction
      , from_stock
      , from_customer
      , to_customer
      , to_stock
      , timestamp
      , bapu_id
      , if_customer
    FROM \`tabReturnable Movement\`
ORDER BY name DESC
 LIMIT 5
;
SELECT 'Showed \`tabReturnable Movement\`\n\n\n' as \`Comment\` \G;

SELECT 
    name
  , docstatus
  , parent
  , idx
  , returnable
  , batch
  , batch_item
  FROM \`tabReturnable Holder\`
 LIMIT 1
 \G

  SELECT 
      name
    , docstatus
    , parent
    , idx
    , returnable
    , batch
    , batch_item
  FROM \`tabReturnable Holder\`
ORDER BY name DESC
 LIMIT 5
;
SELECT 'Showed \`tabReturnable Holder\` \n\n\n' as \`Comment\` \G;

SREOF


    cat << WHEOF > ${QTST_DIR}/qtst.sql

CREATE TEMPORARY TABLE \`tabBottlesFilledAtLeastOnce\` 
  (returnable varchar(140) NOT NULL, PRIMARY KEY(returnable), INDEX(name), INDEX(direction), INDEX(first_move)) AS
  SELECT parent AS returnable, name, direction, MIN(modified) AS first_move, from_stock, to_stock
    FROM  \`tabReturnable Movement\`
   WHERE parent IS NOT NULL
     AND parent != ''
     # AND parent NOT LIKE 'C%'
     AND to_stock IS NOT NULL
     AND direction = 'Stock >> Stock'
GROUP BY parent
ORDER BY parent, modified
;
SELECT * 
  FROM \`tabBottlesFilledAtLeastOnce\`
LIMIT 25;
SELECT 'Showed first FILLING of each returnable from \`tabBottlesFilledAtLeastOnce\`! \n\n\n' as \`Comment\` \G;



CREATE TEMPORARY TABLE \`tabBottlesNeverOnceFilled\` 
  (returnable varchar(140) NOT NULL, PRIMARY KEY(returnable), INDEX(last_move)) AS
   SELECT M.parent AS returnable, MAX(M.NAME) AS last_move
     FROM \`tabReturnable Movement\` M
LEFT JOIN \`tabBottlesFilledAtLeastOnce\` F
       ON M.parent = F.returnable
    WHERE F.returnable IS NULL
      # AND M.parent = @rtrnbl
 GROUP BY M.parent
 ORDER BY M.parent, M.modified
;
SELECT * 
  FROM \`tabBottlesNeverOnceFilled\`
LIMIT 5
;
SELECT 'Showed last move of never filled returnables from \`tabBottlesNeverOnceFilled\`! \n\n\n' as \`Comment\` \G;



CREATE TEMPORARY TABLE \`tabBottlesUnfilledNoLongerUseable\` 
  (returnable varchar(140) NOT NULL, PRIMARY KEY(returnable), INDEX(name), INDEX(modified)) AS
  SELECT parent as returnable, name, direction, from_stock, from_customer, to_customer, to_stock, modified, bapu_id, if_customer
    FROM \`tabReturnable Movement\` M
    JOIN \`tabBottlesNeverOnceFilled\` F
      ON M.parent = F.returnable
     AND M.name = F.last_move
   WHERE 
         direction like '%>> Cust'
     AND to_customer in ('ALERTAR', 'Envases Rotos' )
ORDER BY parent, modified
;
SELECT * 
  FROM \`tabBottlesUnfilledNoLongerUseable\`
LIMIT 5
;

SELECT 'Showed all damaged returnables from \`tabBottlesUnfilledNoLongerUseable\`! \n\n\n' as \`Comment\` \G;


CREATE TEMPORARY TABLE \`tabFirstArrival\` 
  (returnable varchar(140) NOT NULL, PRIMARY KEY(returnable), INDEX(name), INDEX(direction), INDEX(first_move)) AS
   SELECT M.parent AS returnable, M.name, M.direction, MIN(M.modified) AS first_move
     FROM \`tabReturnable Movement\` M
LEFT JOIN \`tabBottlesFilledAtLeastOnce\` F
       ON M.parent = F.returnable
      AND M.to_stock = 'Envases IB Sucios - LSSA'
    WHERE F.returnable IS NOT NULL
 GROUP BY M.parent
 ORDER BY M.parent, M.modified
    # LIMIT 25
;

SELECT * 
  FROM \`tabFirstArrival\`
LIMIT 25
;
SELECT 'Showed first arrival of returnables to stock \`tabFirstArrival\`! \n\n\n' as \`Comment\` \G;

# # SET @rtrnbl := "IBAA002";
SET @rtrnbl := "IBAA004";
SET @rtrnbl := "IBAA011";
SET @rtrnbl := "IBAA013";
SET @rtrnbl := "IBAA026";
SET @rtrnbl := "IBAA027";
SET @rtrnbl := "IBAA058";
SET @rtrnbl := "IBDD433";
SET @rtrnbl := "IBDD040";
SET @rtrnbl := "IBCC511";
SET @rtrnbl := "IBAA664";
  # SELECT M.parent, M.name, M.direction, M.from_stock, M.from_customer, M.to_customer, M.to_stock, M.modified, M.bapu_id, M.if_customer
  SELECT M.parent, MAX(M.modified) AS last_move
    FROM \`tabReturnable Movement\` M
    JOIN \`tabBottlesFilledAtLeastOnce\` F
      ON M.parent = F.returnable
     # AND M.name = F.last_move
   WHERE 
         modified > '2015-12-31 23:12:52.000000'
     # AND parent = @rtrnbl

     # AND direction like '%>> Cust'
     # AND to_customer in ('ALERTAR', 'Envases Rotos' )

     # AND modified > '2016-12-31 23:12:52.000000'
     # AND direction like '%>> Stock'
GROUP BY M.parent
ORDER BY parent, last_move
   LIMIT 25
;

  SELECT parent, name, idx, direction, from_stock, from_customer, to_customer, to_stock, timestamp, bapu_id, if_customer
    FROM \`tabReturnable Movement\` M
   WHERE 
         modified > '2015-12-31 23:12:52.000000'
     AND parent = @rtrnbl
ORDER BY parent, timestamp
   LIMIT 25
;


SELECT CONCAT('Showed all moves of returnable "', @rtrnbl, '"" from \`tabReturnable Movement\`! \n') as \`Comment\` \G;

# SHOW CREATE TABLE \`tabReturnable Movement\`
# ;
# SHOW CREATE TABLE \`tabBottlesFilledAtLeastOnce\`
# ;

  SELECT name, coherente
    FROM \`tabReturnable\` M
   WHERE name in ('IBAA664', 'IBAA665', 'IBAA666')
;

#   UPDATE \`tabReturnable\` M
#    SET coherente = 'Unset'
# ;

WHEOF



    cat << TTEOF > ${QTST_DIR}/qtst.sql

  SELECT coherente, count(name)
    FROM \`tabReturnable\` M
GROUP BY coherente
;

#   UPDATE \`tabReturnable\` M
#      SET coherente = 'Desconocido'
# ;

#   UPDATE \`tabReturnable Movement\` M
#    SET 
#       idx = 4
#   WHERE name = 'RTN-MOV-000000014'
# ;

#   UPDATE \`tabReturnable Movement\` M
#    SET 
#       timestamp = '2016-08-23 17:08:23.000000'
#     , creation = '2016-08-23 17:08:23.000000'
#   WHERE name = 'RTN-MOV-000000014'
# ;

#   UPDATE \`tabReturnable\` M
#    SET coherente = 'Unset'
#   WHERE name = 'IBAA014'
# ;

#   UPDATE \`tabReturnable Movement\` M
#    SET 
#       modified = timestamp
#     , creation = timestamp
#   WHERE parent = 'CLAA018'
# ;

  UPDATE \`tabReturnable\` R
   SET 
      docstatus = 0
;

  UPDATE \`tabReturnable Movement\` M
   SET 
      docstatus = 0
;

#       DELETE FROM \`tabReturnable Movement\`
#        WHERE name = 'RTN-MVX-000000012'
# ;

  SELECT *
    FROM \`tabReturnable Movement\` M
   WHERE parent in ('IBAA255')
ORDER BY parent, timestamp
;

  SELECT max(name)
    FROM \`tabReturnable Movement\` M
ORDER BY timestamp
;

  SELECT max(timestamp)
    FROM \`tabReturnable Movement\` M
   WHERE parent in ('IBAA255')
;

# SHOW CREATE TABLE \`tabReturnable Movement\`
# ;
# SHOW CREATE TABLE \`tabReturnable\`
# ;

      # SELECT max(timestamp) as last_move
      SELECT code,state,times_out,times_in,last_customer,R.bapu_id,fills,last_out,last_move,coherente,M.idx,direction,from_stock,from_customer,to_customer,to_stock,timestamp,if_customer
        FROM \`tabReturnable\` R JOIN \`tabReturnable Movement\` M
          ON R.name = M.parent
       WHERE R.coherente = 'Descartado'
  
;
TTEOF




    cat << UNPAID > ${QTST_DIR}/qtst.sql

#     SELECT 
#            I.name AS Factura
#          , I.customer_name AS Cliente
#          , I.tax_id AS RUC
#          , I.posting_date AS Fecha
#          , TRUNCATE(IFNULL(I.net_total, 0.00), 2) AS Subtotal
#          , TRUNCATE(IFNULL(I.total_taxes_and_charges, 0.00), 2) AS IVA
#          , TRUNCATE(IFNULL(I.grand_total, 0.00), 2) AS Total
#          , I.status AS Estado
#          , TRUNCATE(IFNULL(R.total_amount, 0.00), 2) AS Pagado
#          , TRUNCATE(IFNULL(P.party_balance, 0.00), 2) AS Saldo
#          , REPLACE(P.remarks,'\n', ' ')
#       FROM \`tabSales Invoice\` I
#  LEFT JOIN \`tabPayment Entry Reference\` R
#         ON I.name = R.reference_name
#  LEFT JOIN \`tabPayment Entry\` P
#         ON R.parent = P.name
#      # WHERE I.name < '001-001-000006228'
#      WHERE I.status != 'Paid'
#      ORDER BY I.customer
#      # LIMIT 20
# ;

    SELECT 
           I.customer_name AS Cliente
         , SUM(IFNULL(I.net_total, 0.00)) AS Total
         , SUM(IFNULL(I.total_taxes_and_charges, 0.00)) AS IVA
         , SUM(IFNULL(I.grand_total, 0.00)) AS Total
      FROM \`tabSales Invoice\` I
 LEFT JOIN \`tabPayment Entry Reference\` R
        ON I.name = R.reference_name
 LEFT JOIN \`tabPayment Entry\` P
        ON R.parent = P.name
     WHERE I.status != 'Paid'
       AND IFNULL(I.grand_total, 0.00) > 0.99
       AND IFNULL(I.grand_total, 0.00) > IFNULL(R.total_amount, 0.00)
  GROUP BY Cliente
  ORDER BY Total DESC
INTO OUTFILE '/dev/shm/LSSA/totalsByClientName.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

    SELECT 
           I.name AS Factura
         , I.customer_name AS Cliente
         , I.tax_id AS RUC
         , I.posting_date AS Fecha
         , TRUNCATE(IFNULL(I.net_total, 0.00), 2) AS Subtotal
         , TRUNCATE(IFNULL(I.total_taxes_and_charges, 0.00), 2) AS IVA
         , TRUNCATE(IFNULL(I.grand_total, 0.00), 2) AS Total
         , TRUNCATE(IFNULL(R.total_amount, 0.00), 2) AS Pagado
         , TRUNCATE(IFNULL(P.party_balance, 0.00), 2) AS Saldo
         , I.status AS Estado
         , REPLACE(IFNULL(P.remarks, ''),'\n', ' ') AS Notas
      FROM \`tabSales Invoice\` I
 LEFT JOIN \`tabPayment Entry Reference\` R
        ON I.name = R.reference_name
 LEFT JOIN \`tabPayment Entry\` P
        ON R.parent = P.name
     WHERE I.status != 'Paid'
       AND IFNULL(I.grand_total, 0.00) > 0.99
       AND IFNULL(I.grand_total, 0.00) > IFNULL(R.total_amount, 0.00)
  ORDER BY Cliente
INTO OUTFILE '/dev/shm/LSSA/invoicesByClientName.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

    SELECT 
           I.name AS Factura
         , I.customer_name AS Cliente
         , I.tax_id AS RUC
         , I.posting_date AS Fecha
         , TRUNCATE(IFNULL(I.net_total, 0.00), 2) AS Subtotal
         , TRUNCATE(IFNULL(I.total_taxes_and_charges, 0.00), 2) AS IVA
         , TRUNCATE(IFNULL(I.grand_total, 0.00), 2) AS Total
         , TRUNCATE(IFNULL(R.total_amount, 0.00), 2) AS Pagado
         , TRUNCATE(IFNULL(P.party_balance, 0.00), 2) AS Saldo
         , I.status AS Estado
         , REPLACE(IFNULL(P.remarks, ''),'\n', ' ') AS Notas
      FROM \`tabSales Invoice\` I
 LEFT JOIN \`tabPayment Entry Reference\` R
        ON I.name = R.reference_name
 LEFT JOIN \`tabPayment Entry\` P
        ON R.parent = P.name
     WHERE I.status != 'Paid'
       AND IFNULL(I.grand_total, 0.00) > 0.99
       AND IFNULL(I.grand_total, 0.00) > IFNULL(R.total_amount, 0.00)
  ORDER BY I.grand_total DESC
INTO OUTFILE '/dev/shm/LSSA/worstInvoiceFirst.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;


    SELECT 
           I.name AS Factura
         , I.customer_name AS Cliente
         , I.tax_id AS RUC
         , I.posting_date AS Fecha
         , TRUNCATE(IFNULL(I.net_total, 0.00), 2) AS Subtotal
         , TRUNCATE(IFNULL(I.total_taxes_and_charges, 0.00), 2) AS IVA
         , TRUNCATE(IFNULL(I.grand_total, 0.00), 2) AS Total
         , TRUNCATE(IFNULL(R.total_amount, 0.00), 2) AS Pagado
         , TRUNCATE(IFNULL(P.party_balance, 0.00), 2) AS Saldo
         , I.status AS Estado
         , REPLACE(IFNULL(P.remarks, ''),'\n', ' ') AS Notas
      FROM \`tabSales Invoice\` I
 LEFT JOIN \`tabPayment Entry Reference\` R
        ON I.name = R.reference_name
 LEFT JOIN \`tabPayment Entry\` P
        ON R.parent = P.name
     # WHERE I.name < '001-001-000006228'
     WHERE I.status != 'Paid'
       AND IFNULL(I.grand_total, 0.00) > 0.99
       AND IFNULL(I.grand_total, 0.00) > IFNULL(R.total_amount, 0.00)
  ORDER BY I.name DESC
INTO OUTFILE '/dev/shm/LSSA/chronological.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

# SELECT * FROM \`tabPayment Entry Reference\`
# LIMIT 2\G

# SELECT * FROM \`tabPayment Entry\`
# LIMIT 2\G
UNPAID



# 

    cat << ABEOF > ${QTST_DIR}/qtst.sql

  SELECT LEFT(R.name, 4) AS code, COUNT(*) FROM \`tabReturnable\` R GROUP BY LEFT(R.name, 4); -- LIMIT 4;
ABEOF

    cat << AAEOF > ${QTST_DIR}/qtst.sql
  # SELECT name, idx, bapu_id, direction, timestamp, from_stock, from_customer, to_customer, to_stock, returnables
  #   FROM \`tabReturnable Batch\` B
  #  WHERE B.bapu_id IN ('E_0002830', 'E_0001332')
  #  LIMIT 2;


  # SELECT * FROM \`tabReturnable Batch\` B WHERE B.returnables = 114 LIMIT 5\G
  # SELECT B.bapu_id, MAX(B.returnables) FROM \`tabReturnable Batch\` B WHERE B.bapu_id NOT IN ('IB2020/00843'); 

  # SELECT B.name, M.parent, M.idx, B.direction, B.bapu_id
  #   FROM \`tabReturnable Movement\` M
  #      , \`tabReturnable Batch\` B 
  #  WHERE M.bapu_id = 'ib2020/00877'
  #    AND M.bapu_id = B.bapu_id
  #    AND M.timestamp = B.timestamp
  #  ORDER BY M.idx
  #  ;

  # SELECT count(*)
  #   FROM \`tabReturnable Movement\` M
  #      , \`tabReturnable Batch\` B 
  #  WHERE M.bapu_id = 'ib2020/00877'
  #    AND M.bapu_id = B.bapu_id
  #    AND M.timestamp = B.timestamp
  #  ORDER BY M.idx
  #  ;

  # SELECT * FROM \`tabReturnable Batch\` B WHERE B.bapu_id = 'ib2020/00877'\G 
  # SELECT * FROM \`tabReturnable Movement\` M WHERE M.bapu_id = 'ib2020/00877' LIMIT 1\G

  # SELECT B.name, B.bapu_id, B.returnables FROM \`tabReturnable Batch\` B WHERE B.returnables > 20 AND B.returnables < 30; 

  SELECT R.name, M.idx, B.returnables as Cnt, B.name, M.direction, M.bapu_id, CONCAT(M.bapu_id, '-1'), M.from_stock, M.from_customer, M.to_customer, M.to_stock
    FROM \`tabReturnable\` R
       , \`tabReturnable Movement\` M
       , \`tabReturnable Batch\` B
   WHERE M.parent = R.name
     AND B.bapu_id IN (M.bapu_id, CONCAT(M.bapu_id, '-1')) 
     # AND M.direction = B.direction
     # AND M.from_stock <=> B.from_stock
     # AND M.from_customer <=> B.from_customer
     # AND M.to_customer <=> B.to_customer
     # AND M.to_stock <=> B.to_stock
     # AND M.timestamp = B.timestamp
     AND R.coherente = 'Si'
     AND R.name = 'IBDD571'
ORDER BY R.name, M.idx
   LIMIT 10
;

    SELECT '#', R.name, M.idx, B.returnables, B.flag, M.direction, M.bapu_id, B.bapu_id, M.from_stock, M.from_customer, M.to_customer, M.to_stock
      FROM \`tabReturnable\` R
INNER JOIN \`tabReturnable Movement\` M
            ON M.parent = R.name
 LEFT JOIN \`tabReturnable Batch\` B
            ON B.bapu_id = M.bapu_id
     WHERE R.coherente = 'Si'
     # AND B.bapu_id IN (M.bapu_id, CONCAT(M.bapu_id, '-1')) 
     # AND ( OR B.bapu_id = CONCAT(M.bapu_id, '-1')) 
     # AND B.bapu_id = CONCAT(M.bapu_id, '-1')
       AND M.idx = 1
       AND R.name like 'IBEE%'
  ORDER BY R.name, M.idx
     LIMIT 200
;

#   SELECT count(*)
#     FROM \`tabReturnable\` R
#        , \`tabReturnable Movement\` M
#        , \`tabReturnable Batch\` B
#    WHERE M.parent = R.name
#      AND M.bapu_id = B.bapu_id
#      AND M.direction = B.direction
#      AND M.from_stock <=> B.from_stock
#      AND M.from_customer <=> B.from_customer
#      AND M.to_customer <=> B.to_customer
#      AND M.to_stock <=> B.to_stock
#      AND M.timestamp = B.timestamp
#      AND R.coherente = 'Si'
#      AND R.name = 'IBDD571'
# ORDER BY R.name, M.idx
#    # LIMIT 5
# ;

  # SELECT B.name, B.bapu_id, B.returnables
  # FROM \`tabReturnable Batch\` B
  # WHERE B.bapu_id like 'E_%'
  # ORDER BY B.bapu_id DESC
  # LIMIT 10
  # ;

  # SELECT M.name, M.idx, M.parent, M.direction, M.timestamp, M.bapu_id, M.from_stock, M.from_customer, M.to_customer, M.to_stock
  # FROM \`tabReturnable Movement\` M 
  # WHERE M.bapu_id like 'E_%-1'
  # ORDER BY M.bapu_id DESC
  # # LIMIT 5
  # # ORDER BY M.idx
  # ;

  # # WHERE M.parent = 'IBDD571'  AND M.idx = 4

AAEOF


# 

    cat << ADEOF > ${QTST_DIR}/qtst.sql

    SELECT
            R.name
          , M.name as movement
          , M.idx
          , M.timestamp
          , M.transferred as moved
          , M.direction
          , M.from_stock
          , M.from_customer
          , M.to_customer
          , M.to_stock
          , M.bapu_id
          , B.flag as flagged
          , B.name as batch
          , B.returnables
      FROM \`tabReturnable\` R
INNER JOIN \`tabReturnable Movement\` M
            ON M.parent = R.name
 LEFT JOIN \`tabReturnable Batch\` B
            ON B.bapu_id = M.bapu_id
     WHERE R.coherente = 'Si'
       AND M.idx = 5
       AND M.direction NOT IN ('dummy')
       # AND R.name like 'CLAA%'
       # AND R.name like 'CLCC%'
       AND R.name like 'IBAA%'
       # AND R.name like 'IBCC%'
       # AND R.name like 'IBDD%'
       # AND R.name like 'IBEE%'
  ORDER BY R.name, M.idx
       LIMIT 0, 7;

    SELECT
            M.name as movement
          , M.transferred as moved
          , M.bapu_id
          , B.bapu_id
          , B.flag as flagged
          , B.name as batch
          , B.returnables
      FROM \`tabReturnable Movement\` M
 LEFT JOIN \`tabReturnable Batch\` B
            ON B.bapu_id = M.bapu_id
     WHERE B.name = "RTN-BCH-000012128"
  # ORDER BY R.name, M.idx
       # LIMIT 0, 7
;

SELECT * FROM \`tabReturnable Batch Item\` LIMIT 0, 1\G

UPDATE \`tabReturnable Batch\` set docstatus = 0;

SELECT * FROM \`tabReturnable Batch\` LIMIT 0, 1\G
ADEOF


# 
    cat << AEEOF > ${QTST_DIR}/qtst.sql
# SELECT *
#   FROM \`tabStock Entry Detail\`
#  # WHERE stock_entry_type = 'Material Transfer'
#  LIMIT 0,2
# \G
SELECT *
  FROM \`tabStock Entry\` E,  \`tabStock Entry Detail\` D
 WHERE E.name = D.parent
   AND E.stock_entry_type = 'Material Transfer'
   AND D.transfer_qty > 1
 LIMIT 0,2
\G

ALTER TABLE \`tabStock Entry Detail\`
DROP INDEX IF EXISTS serial_no;

ALTER TABLE \`tabStock Entry Detail\`
ADD FULLTEXT(serial_no)
;

SHOW INDEX FROM \`tabStock Entry Detail\`
;

UPDATE \`tabStock Entry\`
   SET remarks = '{ "direction": "Stock >> Stock", "bapu_id": "2019/3456" }', docstatus = 0
 WHERE name = 'MAT-STE-2020-00038'
;

SET @returnable = 'IBAA584';
SELECT
         @returnable as Envase
       , JSON_EXTRACT(IFNULL(E.remarks, '{ "direction": "??", "bapu_id": "??" }'), '$.direction')  as Direccion
       , D.parent as Movimiento
       , D.s_warehouse as Origen
       , D.t_warehouse as Destino
       , D.creation as Fecha
       , E.stock_entry_type as Tipo
       , JSON_EXTRACT(IFNULL(E.remarks, '{ "direction": "??", "bapu_id": "??" }'), '$.bapu_id')  as BAPU
       , REPLACE(D.serial_no, '\n', ' ')
  FROM \`tabStock Entry\` E, \`tabStock Entry Detail\` D
 WHERE D.parent = E.name
   AND D.item_code = 'Envase de 5GL Iridium Blue'
   AND MATCH(serial_no) AGAINST(@returnable)
   ORDER BY D.creation desc
;

select count(*) from \`tabStock Entry\` limit 0,1\G

AEEOF



# 



# 

    cat << AZEOF > ${QTST_DIR}/qtst.sql

#     SELECT 
#            I.customer_name AS Cliente
#          , SUM(IFNULL(I.net_total, 0.00)) AS Total
#          , SUM(IFNULL(I.total_taxes_and_charges, 0.00)) AS IVA
#          , SUM(IFNULL(I.grand_total, 0.00)) AS Total
#       FROM \`tabSales Invoice\` I
#  LEFT JOIN \`tabPayment Entry Reference\` R
#         ON I.name = R.reference_name
#  LEFT JOIN \`tabPayment Entry\` P
#         ON R.parent = P.name
#      WHERE I.status != 'Paid'
#        AND IFNULL(I.grand_total, 0.00) > 0.99
#        AND IFNULL(I.grand_total, 0.00) > IFNULL(R.total_amount, 0.00)
#   GROUP BY Cliente
#   ORDER BY Total DESC
# INTO OUTFILE '/dev/shm/LSSA/totalsByClientName.csv'
# FIELDS TERMINATED BY ','
# ENCLOSED BY '"'
# LINES TERMINATED BY '\n'
# ;

#     SELECT 
#            I.name AS Factura
#          , I.customer_name AS Cliente
#          , I.tax_id AS RUC
#          , I.posting_date AS Fecha
#          , TRUNCATE(IFNULL(I.net_total, 0.00), 2) AS Subtotal
#          , TRUNCATE(IFNULL(I.total_taxes_and_charges, 0.00), 2) AS IVA
#          , TRUNCATE(IFNULL(I.grand_total, 0.00), 2) AS Total
#          , TRUNCATE(IFNULL(R.total_amount, 0.00), 2) AS Pagado
#          , TRUNCATE(IFNULL(P.party_balance, 0.00), 2) AS Saldo
#          , I.status AS Estado
#          , REPLACE(IFNULL(P.remarks, ''),'\n', ' ') AS Notas
#       FROM \`tabSales Invoice\` I
#  LEFT JOIN \`tabPayment Entry Reference\` R
#         ON I.name = R.reference_name
#  LEFT JOIN \`tabPayment Entry\` P
#         ON R.parent = P.name
#      WHERE I.status != 'Paid'
#        AND IFNULL(I.grand_total, 0.00) > 0.99
#        AND IFNULL(I.grand_total, 0.00) > IFNULL(R.total_amount, 0.00)
#   ORDER BY Cliente
# # INTO OUTFILE '/dev/shm/LSSA/invoicesByClientName.csv'
# # FIELDS TERMINATED BY ','
# # ENCLOSED BY '"'
# # LINES TERMINATED BY '\n'
# ;

#     SELECT 
#            I.name AS Factura
#          , I.customer_name AS Cliente
#          , I.tax_id AS RUC
#          , I.posting_date AS Fecha
#          , TRUNCATE(IFNULL(I.net_total, 0.00), 2) AS Subtotal
#          , TRUNCATE(IFNULL(I.total_taxes_and_charges, 0.00), 2) AS IVA
#          , TRUNCATE(IFNULL(I.grand_total, 0.00), 2) AS Total
#          , TRUNCATE(IFNULL(R.total_amount, 0.00), 2) AS Pagado
#          , TRUNCATE(IFNULL(P.party_balance, 0.00), 2) AS Saldo
#          , I.status AS Estado
#          , REPLACE(IFNULL(P.remarks, ''),'\n', ' ') AS Notas
#       FROM \`tabSales Invoice\` I
#  LEFT JOIN \`tabPayment Entry Reference\` R
#         ON I.name = R.reference_name
#  LEFT JOIN \`tabPayment Entry\` P
#         ON R.parent = P.name
#      WHERE I.status != 'Paid'
#        AND IFNULL(I.grand_total, 0.00) > 0.99
#        AND IFNULL(I.grand_total, 0.00) > IFNULL(R.total_amount, 0.00)
#   ORDER BY I.grand_total DESC
# # INTO OUTFILE '/dev/shm/LSSA/worstInvoiceFirst.csv'
# # FIELDS TERMINATED BY ','
# # ENCLOSED BY '"'
# # LINES TERMINATED BY '\n'
# ;


    SELECT 
           I.name AS Factura
         , IFNULL(I.po_no, I.name) AS BAPU_ID 
         , I.customer_name AS Cliente
         , I.tax_id AS RUC
         , I.posting_date AS Fecha
         , TRUNCATE(IFNULL(I.net_total, 0.00), 2) AS Subtotal
         , TRUNCATE(IFNULL(I.total_taxes_and_charges, 0.00), 2) AS IVA
         , TRUNCATE(IFNULL(I.grand_total, 0.00), 2) AS Total
         , TRUNCATE(IFNULL(R.total_amount, 0.00), 2) AS Pagado
         , TRUNCATE(IFNULL(P.party_balance, 0.00), 2) AS Saldo
         , I.status AS Estado
         , REPLACE(IFNULL(P.remarks, ''),'\n', ' ') AS Notas
      FROM \`tabSales Invoice\` I
 LEFT JOIN \`tabPayment Entry Reference\` R
        ON I.name = R.reference_name
 LEFT JOIN \`tabPayment Entry\` P
        ON R.parent = P.name
     # WHERE IFNULL(I.grand_total, 0.00) > 0.99
     #   AND IFNULL(I.grand_total, 0.00) > IFNULL(R.total_amount, 0.00)
  ORDER BY I.name
INTO OUTFILE '/dev/shm/LSSA/allInvoices.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

    # SELECT name, po_no, customer_name
    #   FROM \`tabSales Invoice\` I
    #  WHERE name = '001-002-000004086'
    # LIMIT 0,1
    # \G

    # SELECT name, po_no, customer_name
    #   FROM \`tabSales Invoice\` I
    #  WHERE name = '001-002-000004086'
    # LIMIT 0,1
    # \G
AZEOF

    cat << AYEOF > ${QTST_DIR}/InvoicesSelling5GlIBjugs.sql
  SELECT S.name, S.customer_name, I.item_code, FORMAT(I.qty, 0 ), FORMAT(I.net_rate, 2 )
    FROM \`tabSales Invoice\` S, \`tabSales Invoice Item\` I
   WHERE I.parent = S.name
     AND I.item_code like 'Envase%Iridium Blue%'
ORDER BY S.name
INTO OUTFILE '/dev/shm/LSSA/InvoicesSelling5GlIBjugs.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

#   SELECT S.customer_name AS Cliente, I.item_code AS Item, I.net_rate AS Precio, SUM(I.qty) AS qty
#     FROM \`tabSales Invoice\` S, \`tabSales Invoice Item\` I
#    WHERE I.parent = S.name
#      AND I.item_code like 'Envase%Iridium Blue%'
# GROUP BY S.customer_name, I.item_code, I.net_rate
# ORDER BY S.customer_name, I.item_code, I.net_rate
# ;
# #    LIMIT 0, 1
# # \G    
AYEOF

cat << ADEOF > ${QTST_DIR}/AcquisitionDates.sql
    DROP TABLE IF EXISTS \`firstUses\`;
    CREATE TEMPORARY TABLE \`firstUses\` AS 
        SELECT 
               EXTRACT(YEAR_MONTH FROM min(M.timestamp)) as YearMonth
             , M.timestamp AS FirstUse
             , R.name as Returnable
          FROM \`tabReturnable\` R, \`tabReturnable Movement\` M
         WHERE M.parent = R.name
      GROUP BY R.name
      ORDER BY Returnable;

    DROP TABLE IF EXISTS acquisitionMonths;
    CREATE TEMPORARY TABLE acquisitionMonths AS SELECT YearMonth, count(*) as Cnt from \`firstUses\` GROUP BY YearMonth;

    DROP TABLE IF EXISTS ranges;
    CREATE TEMPORARY TABLE ranges AS  SELECT YearMonth, Cnt,
        CASE WHEN YearMonth < '201602' THEN '201512'
             WHEN YearMonth < '201612' THEN '201602'
             WHEN YearMonth < '201704' THEN '201612'
             WHEN YearMonth < '201805' THEN '201704'
             WHEN YearMonth < '201808' THEN '201805'
             WHEN YearMonth < '202012' THEN '201808'
          ELSE YearMonth
        END AS Acquired
        FROM acquisitionMonths;

    DROP TABLE IF EXISTS acquisitions;
    CREATE TABLE acquisitions AS
          SELECT 
              R.Acquired
            , R.YearMonth
            , F.Returnable
            , F.FirstUse
            , CONCAT(SUBSTRING(R.Acquired, 1, 4), '-', SUBSTRING(R.Acquired, 5, 2), '-01') as DateAcquired
            FROM
               \`firstUses\` F
            , ranges AS R
           WHERE R.YearMonth = F.YearMonth
        ORDER BY F.Returnable;

    # SELECT * FROM \`firstUses\` F LIMIT 15;
    # SELECT * FROM ranges R;
    # SELECT * FROM acquisitions A LIMIT 25;

    # SELECT R.name, R.acquisition, A.Acquired, CONCAT(SUBSTRING(A.Acquired, 1, 4), '-', SUBSTRING(A.Acquired, 5, 2), '-01') FROM \`tabReturnable\` R, acquisitions A WHERE R.name = A.Returnable limit 10;

    UPDATE \`tabReturnable\` R
    SET
      R.acquisition = (SELECT CONCAT(SUBSTRING(A.Acquired, 1, 4), '-', SUBSTRING(A.Acquired, 5, 2), '-01') FROM acquisitions A WHERE R.name = A.Returnable);
ADEOF



    cat << QQEOF > ${QTST_DIR}/GetAcquisitionDates.sql
  # SELECT * FROM acquisitions A WHERE Returnable like 'IBCC23%';
  # SELECT A.DateAcquired, count(Returnable) FROM acquisitions A GROUP BY Acquired;
  SELECT acquisition, count(name) FROM \`tabReturnable\` R GROUP BY acquisition;


  -- LIMIT 25;
QQEOF






    cat << QREOF > ${QTST_DIR}/GetBatchDates.sql
  SELECT * FROM \`tabReturnable Batch\` R WHERE timestamp BETWEEN "2021-02-02 00:00:00" AND "2021-02-02 23:59:59" ORDER BY timestamp LIMIT 20;
  SELECT
            R.name
          , R.bapu_id
          , R.timestamp
          , R.direction
          , R.from_stock
          , R.from_customer
          , R.to_customer
          , R.to_stock
          , R.returnables
    FROM \`tabReturnable Batch\` R ORDER BY R.timestamp DESC LIMIT 20;
  SELECT bottle FROM \`tabReturnable Batch Item\` R WHERE parent = "RTN-BCH-000051189" LIMIT 20;
QREOF

    cat << QSEOF > ${QTST_DIR}/OrderAllMovementsByTimeStamp.sql
  SELECT parent, direction, timestamp, substring(timestamp, 1, 10) as date, if(bapu_id = "", CONCAT("ERP", REPLACE(substring(timestamp, 1, 10), "-", "")), bapu_id) as bapu_id, if_customer 
    FROM \`tabReturnable Movement\`
   WHERE timestamp > '2019-02-04'
ORDER BY timestamp
   LIMIT 40;  

  SELECT SQL_CALC_FOUND_ROWS
            substring(timestamp, 1, 10) as date
          , if(bapu_id = "", CONCAT("ERP", REPLACE(substring(timestamp, 1, 10), "-", "")), bapu_id) as bapu_id
          , COUNT(parent) AS Bottles
    FROM \`tabReturnable Movement\`
   WHERE direction = "Stock >> Stock"
GROUP BY date, bapu_id
ORDER BY date, bapu_id
   # LIMIT 40
   ;

SELECT FOUND_ROWS();

SELECT CONCAT('Create returnable locator\n') as \`Comment\` \G;
DROP TABLE IF EXISTS locator;
    CREATE TEMPORARY TABLE locator ENGINE=MEMORY
        AS SELECT code,  state
      FROM \`tabReturnable\`
     LIMIT 10,2
    ;  

  SELECT count(*)
    FROM \`tabReturnable Movement\`
    ;  

  SELECT parent, direction
    FROM \`tabReturnable Movement\`
    LIMIT 20
    ;  

SELECT parent, direction, timestamp FROM \`tabReturnable Movement\` ORDER BY timestamp LIMIT 0, 5;
SELECT parent, direction, timestamp FROM \`tabReturnable Movement\` ORDER BY timestamp LIMIT 5, 5;


#  SELECT code,  state
#       FROM \`tabReturnable\`
#     WHERE state NOT IN ('Lleno', 'Sucio', 'Confuso', 'Donde Cliente')  
#      LIMIT 10,2
# ;

# DROP TABLE IF EXISTS locator;
#     CREATE TABLE Movements AS
#         SELECT *
#         FROM \`tabReturnable Movement\`
#         WHERE timestamp > '2021-01-29 15:24:14.000000'
#         ORDER BY timestamp
#     ;

delete from \`tabReturnable Movement\` where name =  '562db5485f';

QSEOF

if [[ -f envars.sh ]]; then
    source  envars.sh;
    # mysql -t ${1} < ${QTST_DIR}/qtst.sql;
    # mysql -t ${1} < ${QTST_DIR}/InvoicesSelling5GlIBjugs.sql;
    # mysql -t ${ERPNEXT_SITE_DB} < ${QTST_DIR}/AcquisitionDates.sql;
    # mysql -t ${ERPNEXT_SITE_DB} < ${QTST_DIR}/GetAcquisitionDates.sql;

    # mysql -t ${ERPNEXT_SITE_DB} < ${QTST_DIR}/GetBatchDates.sql;

    mysql -t ${ERPNEXT_SITE_DB} < ${QTST_DIR}/OrderAllMovementsByTimeStamp.sql;

else 
    echo -e "Found NO symbolic link 'envars.sh' to an environment variables file.";
fi;


fi;


echo -e "/*  ~~~~~~~~~ Curtailed ~~~~~~~ ${SCRIPT_NAME} ~~~~~~~~  */";
exit;


