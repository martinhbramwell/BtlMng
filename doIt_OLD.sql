SET @pretty = "\n**************************************************************";


select "" as "", "" as "", "" as "", "____________________________________________________________" as ""\G
--         *************************** 1. row ***************************
select concat("Get Last importation Stock Entry                         *", @pretty) as "* "\G

select ifnull(max(bapu_id), 'MAT-STE-2022-00481'), modified  from `tabReturnable Movement` where modified > "2022-07-11 11:03:35.000000";



select "" as "", "" as "", "" as "", "____________________________________________________________" as ""\G
--         *************************** 1. row ***************************
select concat("Get relevant details from Stock Entry                    *", @pretty) as "* "\G
select 
      SE.name
    , SED.item_code
    , SED.s_warehouse
    , SED.t_warehouse
    , REPLACE(SED.serial_no,'\n',', ') as serial_no
from
    `tabStock Entry` SE left join `tabStock Entry Detail` SED 
       on SED.parent = SE.name
where
   SE.name > (
        select ifnull(max(bapu_id), 'MAT-STE-2022-00481')
          from `tabReturnable Movement`
         where modified > "2022-07-11 11:03:35.000000"
    )
  and
    item_code in (
        select distinct required_accompaniment
        from `tabItem`
        where required_accompaniment is not null
    )
order by SE.name asc
limit 6
;


-- select "" as "", "" as "", "" as "", "____________________________________________________________" as ""\G
-- --         *************************** 1. row ***************************
-- select concat("Examine Stock Entry attributes                           *", @pretty) as "* "\G
-- select
--     *
-- from
--     `tabStock Entry` SE left join `tabStock Entry Detail` SED 
--        on SED.parent = SE.name
-- where item_code = "FICHA - para envase IB de 5GL"
-- and SE.name < "MAT-STE-2022-00483"
-- -- and SE.owner != "Administrator"
-- order by SE.posting_date desc, SE.posting_time desc
-- -- ;
-- limit 1
-- \G

-- --         *************************** 1. row ***************************
-- select concat("Examine Stock Entry attributes                           *", @pretty) as "* "\G

-- select "" as "", "" as "", "" as "", "____________________________________________________________" as ""\G
-- --         *************************** 1. row ***************************
-- select concat("Examine Returnable Movement attributes                   *", @pretty) as "* "\G
-- /*
-- select 
--       name
--     , parent
--     , idx
--     , direction
--     , from_stock
--     , from_customer
--     , to_customer
--     , to_stock
--     , timestamp
--     , if_customer
-- */
-- select *
-- from `tabReturnable Movement`
-- order by timestamp desc
-- -- where parent = "IBAA036"
-- -- order by idx asc
-- limit 1
-- \G
-- -- ;


select "" as "", "" as "", "" as "", "____________________________________________________________" as ""\G
--         *************************** 1. row ***************************
select concat("Examine Returnable Movement attributes                   *", @pretty) as "* "\G
select 
      name
    , parent
    , idx
from `tabReturnable Movement`
where parent = "IBAA049"
order by name;

select @count := max(idx)
from `tabReturnable Movement`
where parent = "IBAA049"
order by idx asc
;

-- select @count := 7;
select @count;

-- ALTER TABLE `tabReturnable Movement` ADD INDEX ret_idx (parent, idx);
describe update `tabReturnable Movement` A set idx = (select max(idx) from `tabReturnable Movement` B where A.parent = B.parent) - idx + 1; # where A.parent in ("IBAA038", "IBAA049");
-- update `tabReturnable Movement` A set idx = (select max(idx) from `tabReturnable Movement` B where A.parent = B.parent) - idx + 1; # where A.parent in ("IBAA038", "IBAA049");

-- set @bottle:="IBCC372";
-- --         *************************** 1. row ***************************
-- select concat(left(concat("Movements for bottle: ", @bottle, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G
-- select 
--         -- *
--       name
--     , parent
--     , idx
--     , bapu_id
--     , from_stock
--     , from_customer
--     , to_customer
--     , to_stock
--     , parentfield
-- from `tabReturnable Movement`
-- -- where parent in ("IBAA049")
-- where parent in ("IBCC372")
-- order by idx desc
-- ;
-- select concat(left(concat("Movements for bottle: ", @bottle, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G


-- select concat(left(concat("Total moves for bottle: ", @bottle, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G
-- select count(*) as Movements
-- from `tabReturnable Movement`
-- where parent in (@bottle)
-- ;
-- select concat(left(concat("Total moves for bottle: ", @bottle, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G


-- select concat(left(concat("Fillings for bottle: ", @bottle, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G
-- select count(*) as Fillings
-- from `tabReturnable Movement`
-- where parent in (@bottle)
--   and direction = "Stock >> Stock"
-- ;


-- select concat(left(concat("Departures for bottle: ", @bottle, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G
-- select count(*) as Departures
-- from `tabReturnable Movement`
-- where parent in (@bottle)
--   and direction = "Stock >> Cust"
-- ;
-- select concat(left(concat("Departures for bottle: ", @bottle, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G


-- select concat(left(concat("Arrivals for bottle: ", @bottle, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G
-- select count(*) as Arrivals
-- from `tabReturnable Movement`
-- where parent in (@bottle)
--   and direction = "Cust >> Stock"
-- ;
-- select concat(left(concat("Arrivals for bottle: ", @bottle, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G


-- select max(name)
-- from `tabReturnable Movement`
-- ;


-- select * from tabSeries;
set @bottle1:="IBEE076";
set @bottle2:="IBEE063";
set @bottle3:="IBEE081";

set @MSG = "Bottle Movements To/From Customers";
select concat(left(concat(@MSG, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G

-- select 
--     --   name
--     -- , parent
--     -- , idx
--     -- , direction
--     -- , from_stock
--     -- , from_customer
--     -- , to_customer
--     -- , to_stock
--     -- , if_customer
--     concat("update `tabReturnable Movement` set "
--         , if (direction = "Stock >> Cust"
--                 , concat("to_customer = '", to_customer, " - LSSA'", ", if_customer = '", if_customer, " - LSSA'")
--                 , concat("from_customer = '", from_customer, " - LSSA'", ", if_customer = '", if_customer, " - LSSA'")
--             )
--         , " where name = '", name, "';") as update2
--     into outfile "/dev/shm/moveUpdates.sql"
-- from `tabReturnable Movement`
-- where if_customer is not null
--   and ( to_customer not like "% - LSSA%" or from_customer not like "% - LSSA%" )
--   -- and parent in (@bottle1, @bottle2, @bottle3)
-- ;


-- select * from `tabReturnable Movement` limit 1;
select * from `tabWarehouse` limit 1\G
select distinct M.if_customer, W.name from `tabReturnable Movement` M left join `tabWarehouse` W on M.if_customer = W.name  where M.if_customer is not null and W.name is null limit 12;

select concat(left(concat(@MSG, REPEAT(' ', 60)), 57), "*", @pretty) as "* "\G


select distinct required_accompaniment
from `tabItem`
where required_accompaniment is not null
;

select @id := ifnull(max(bapu_id), 'MAT-STE-2022-00481')
  from `tabReturnable Movement`
 where creation > "2022-07-11 11:03:34.000000"
;


select @id;

select @next_id := SE.name
from
    `tabStock Entry` SE left join `tabStock Entry Detail` SED 
       on SED.parent = SE.name
where
   SE.name > @id
order by SE.name asc
limit 1
;

select 
      SE.name
    , SE.posting_date
    , SE.posting_time
    , SED.item_code
    , SED.s_warehouse
    , SED.t_warehouse
    , SED.serial_no
from
    `tabStock Entry` SE left join `tabStock Entry Detail` SED 
       on SED.parent = SE.name
where
   SE.name = @next_id
  and
    item_code in (
        select distinct required_accompaniment
        from `tabItem`
        where required_accompaniment is not null
    )
order by SE.name asc
;

  select @ABBR := abbr
    from `tabCompany`
where name like '%Logichem%'
;

  select REPLACE(if_customer, concat(' - ', @ABBR), '')
    from `tabReturnable Movement`
   where parent = 'IBAA881'
     and if_customer is not null
order by idx asc
   limit 1
;




select "" as "", "" as "", "" as "", "============================================================" as ""\G

