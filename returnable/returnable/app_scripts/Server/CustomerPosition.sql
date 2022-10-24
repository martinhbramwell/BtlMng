-- DROP TABLE IF EXISTS CustomerPayments;

-- CREATE OR REPLACE VIEW CustomerPayments
-- AS select
--         party
--       , count(PE.name) Payments 
--       , sum(PE.paid_amount) Paid
--  from `tabPayment Entry` PE
--  group by party
-- ;

-- CREATE OR REPLACE VIEW CustomerInvoices
-- AS select
--         customer
--       , count(SI.name) Invoices
--       , sum(SI.grand_total) as Owed
--  from `tabSales Invoice` SI 
--  group by customer
-- ;


-- CREATE OR REPLACE VIEW CustomerPosition
-- AS select
-- 	  customer as Cliente
-- 	, Invoices as Facturas
-- 	, Owed as Comprado
-- 	, IFNULL(Payments, 0) as Pagos
-- 	, IFNULL(Paid, 0) as Pagado
-- 	, Owed - IFNULL(Paid, 0) as Debido
--  from CustomerInvoices 
--  left join CustomerPayments
--          on customer = party
-- where Owed - IFNULL(Paid, 0) NOT BETWEEN -0.0001 AND 0.0001
-- ;


--  SELECT *
--     FROM CustomerPosition
-- GROUP BY Cliente
-- ORDER BY Debido asc
-- LIMIT 30
-- ;
 
-- -- mysql 
-- --  --skip-column-names --batch -e '

-- -- select CONCAT("DROP TABLE IF EXISTS ", TABLE_SCHEMA, ".", TABLE_NAME, "; CREATE OR REPLACE VIEW ", TABLE_SCHEMA, ".", TABLE_NAME, " AS ", VIEW_DEFINITION, "; ") 
-- -- FROM information_schema.views
-- -- WHERE table_schema = (SELECT database() FROM dual)
-- -- ;


--   SELECT ifnull(Debido, 0) as Debido, 1
--     FROM CustomerPosition
--    WHERE Cliente = "Oyempaques C.A."
-- ;

-- --        INTO OUTFILE '/dev/shm/CustomerPosition.csv'
-- -- FIELDS TERMINATED BY ','
-- --          ENCLOSED BY '"'
-- --  LINES TERMINATED BY '\n'
-- -- ;

-- select
--         customer
--       , SI.name Invoices
--       , sum(SI.grand_total) as Owed
--  from `tabSales Invoice` SI 
--  group by customer
-- ;

select * from `tabSales Invoice` SI\G
