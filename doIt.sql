SET @pretty = "\n**************************************************************";

SELECT "" as "", "" as "", "" as "", "____________________________________________________________" as ""\G
--         *************************** 1. row ***************************
SELECT concat("Get Next Stock Entry                                     *", @pretty) as "* "\G

select SE.name as next_entry, SED.item_code as item
from
    `tabStock Entry` SE left join `tabStock Entry Detail` SED 
       on SED.parent = SE.name
where
   SE.name > 'MAT-STE-2022-01532'
  -- and
  --   item_code in (
  --       select distinct required_accompaniment
  --       from `tabItem`
  --       where required_accompaniment is not null
  --   )
order by SE.name asc
limit 1
;

SELECT "" as "", "" as "", "" as "", "____________________________________________________________" as ""\G
--         *************************** 1. row ***************************
SELECT concat("Get Latest Returnable Movement                           *", @pretty) as "* "\G

select ifnull(max(bapu_id), 'MAT-STE-2022-00481') as latest
  from `tabReturnable Movement`
 where creation > "2022-07-11 11:03:34.000000"
;

-- delete from `tabReturnable Movement`
select name, creation, modified, timestamp, parent, direction, bapu_id, if_customer  from `tabReturnable Movement`
 where name like "RET-MOV-%"
   and bapu_id like "MAT-STE-%"
;



set @FICHA = "IBAA892";

select parent, idx
  from `tabReturnable Movement` B
where B.parent in (@FICHA);


DROP INDEX IF EXISTS ret_idx on `tabReturnable Movement`;
ALTER TABLE `tabReturnable Movement` ADD INDEX ret_idx (parent, idx);
-- describe update `tabReturnable Movement` A set idx = (select max(idx) from `tabReturnable Movement` B where A.parent = B.parent) - idx + 1; # where A.parent in ("IBAA038", "IBAA049");


update `tabReturnable Movement` A 
   set idx = (
       select max(idx)
         from `tabReturnable Movement` B
        where A.parent = B.parent
     ) - idx + 1
-- where A.parent BETWEEN "IBAA060" AND "IBAA065"
where A.parent in (@FICHA)
;


select parent, idx, timestamp
  from `tabReturnable Movement` B
where B.parent in (@FICHA);


-- select parent, count(name), max(idx), min(idx), min(timestamp), max(timestamp)
--   from `tabReturnable Movement` B
-- where B.parent BETWEEN "IBAA001" AND "IBAA099"
-- group by B.parent
-- HAVING min(idx) > 1 OR max(idx) != count(name)
-- ;

select A.parent, A.timestamp, B.idx, B.timestamp
  from `tabReturnable Movement` A left join `tabReturnable Movement` B
    on A.parent = B.parent
-- where A.parent BETWEEN "IBAA060" AND "IBAA065"
where A.timestamp < B.timestamp
  and A.idx = 1
  and B.idx = (
       select max(C.idx)
         from `tabReturnable Movement` C
       where C.parent = A.parent and C.parent = B.parent
  )
;


SELECT "" as "", "" as "", "" as "", "============================================================" as ""\G

