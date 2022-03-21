drop table if exists Invoice;
create temporary table Invoice as
select 
	SI.name, SI.customer_name, SI.posting_date, SII.item_code, FLOOR(SII.qty) AS Qty
from
	`tabSales Invoice` SI
left join
	`tabSales Invoice Item` SII
	on SI.name = SII.parent
where
	SI.name between "001-002-000007511"
	     and "001-002-000007550"
;
select * from Invoice;


drop table if exists Move;
create temporary table Move as
select
	    B.name
	  , B.to_customer
	  , left(B.timestamp, 10) as Date
#	  , I.idx
	  , group_concat(I.bottle separator ',') as SN
from
	`tabReturnable Batch` B
left join
	`tabReturnable Batch Item` I
	on B.name = I.parent
where
	B.direction = 'Stock >> Cust'
and
	B.name between "RTN-BCH-000060639"
	     and "RTN-BCH-000060791"
group by B.name
order by B.name, I.idx
# limit 2
;
select * from Move limit 16;


#############  For sales order:
drop table if exists SalesOrder;
create temporary table SalesOrder as
select 
	  concat('{
    "customer": "', M.to_customer,'",
    "customer_name": "', M.to_customer,'",
    "delivery_date": "', date(adddate(now(), interval 1 week)),'",
    "items": [') as soCustomer
 	, group_concat(concat('{
            "item_code": "', I.item_code, '",
            "qty": ', I.qty, '
       }') separator ',') as Items
       , ']
}' as soClose       
from
	Move M
left join
	Invoice I
on
	I.customer_name = M.to_customer
where
	I.customer_name in ("Julien Reynaud", "Yael Esmeralda Cerda Verdesoto", "Luis Eduardo Cordovez", "Maria Correa")
group by soCustomer
;
select * from SalesOrder;
select concat(soCustomer, Items, soClose) as "" from SalesOrder\G



#############  For delivery note:
select distinct
	  concat('"', M.to_customer, '": `', REPLACE(SN, ",", "\\n"), '`,') as JS
from
	Move M
left join
	Invoice I
on
	I.customer_name = M.to_customer
where
	I.customer_name in ("Julien Reynaud", "Jose Fabian Cordova", "Luis Eduardo Cordovez", "Maria Correa")
\G




