# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

import sys
import frappe
import datetime


qryLatestReturnableMovement = f"""
    select ifnull(max(bapu_id), 'MAT-STE-2022-00481') as latest
      from `tabReturnable Movement`
     where creation > "2022-07-11 11:03:34.000000"
"""

def qryNextStockEntry(latest):
    return f"""
        select SE.name as next_entry
        from
            `tabStock Entry` SE left join `tabStock Entry Detail` SED 
               on SED.parent = SE.name
        where
           SE.name > '{latest}'
          and
            item_code in (
                select distinct required_accompaniment
                from `tabItem`
                where required_accompaniment is not null
            )
        order by SE.name asc
        limit 1
    """

def qryStockEntry(next_entry):
    return f"""
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
           SE.name = "{next_entry}"
          and
            item_code in (
                select distinct required_accompaniment
                from `tabItem`
                where required_accompaniment is not null
            )
        order by SED.name asc
    """

STOCK = "Stock"
CUST = "Cust"

def getOneStockEntry():
    stockEntryDetails = None
    moves = frappe.db.sql(qryLatestReturnableMovement, as_dict=1)

    if moves is not None:
        latest = moves[0].latest
        # latest = 'MAT-STE-2022-00513'
        # print(latest)

        stockEntry = frappe.db.sql(qryNextStockEntry(latest), as_dict=1)

        if stockEntry:
            # print('stockEntry')
            # print(stockEntry)
            # print(stockEntry[0].next_entry)

            stockEntryDetails = frappe.db.sql(qryStockEntry(stockEntry[0].next_entry), as_dict=1)
            # print(stockEntryDetails)
        else:
            print("Found no Stock Entries")

    return stockEntryDetails

def incrementReturnableMovementIndexes(serial_no):
    return """
        update `tabReturnable Movement`
        set idx = idx + 1
        where parent = {sn}
    """.format(sn = frappe.db.escape(serial_no))

def getReturnableMoveCount(serial_no):
    qry = f"""
        select count(*)
        from `tabReturnable Movement`
        where parent = '{serial_no}'
    """ 
    return frappe.db.sql(qry)[0][0]

def getReturnableFillingsCount(serial_no):
    qry = f"""
        select count(*)
          from `tabReturnable Movement`
         where parent = '{serial_no}'
           and direction = "Stock >> Stock"
    """ 
    return frappe.db.sql(qry)[0][0]

def getReturnableDeparturesCount(serial_no):
    qry = f"""
        select count(*)
          from `tabReturnable Movement`
         where parent = '{serial_no}'
           and direction = "Stock >> Cust"
    """ 
    return frappe.db.sql(qry)[0][0]

def getReturnableArrivalsCount(serial_no):
    qry = f"""
        select count(*)
          from `tabReturnable Movement`
         where parent = '{serial_no}'
           and direction = "Cust >> Stock"
    """ 
    return frappe.db.sql(qry)[0][0]

def reformatStockEntryDetail(sed):
    print(f" - Stock Entry :: {sed.name}")
    print(sed)

    source = ""
    target = ""

    move = {
        "direction": "",
        "idx": 0,
        "parentfield": "moves",
        "from_stock": "",
        "from_customer": "",
        "to_customer": "",
        "to_stock": "",
        "timestamp": "",
        "if_customer": ""
    }

    if not sed.s_warehouse and sed.t_warehouse == "Envases IB Llenos - LSSA":
        sed.s_warehouse = "Envases IB Sucios - LSSA"

    if "Envases IB" in sed.s_warehouse:
        source = STOCK
        move["from_stock"] = sed.s_warehouse
        move["from_customer"] = None
        move["if_customer"] = None
    else:
        source = CUST
        move["from_stock"] = None
        move["from_customer"] = sed.s_warehouse
        move["if_customer"] = sed.s_warehouse

    if not sed.t_warehouse and sed.s_warehouse == "Envases IB Sucios - LSSA":
        sed.t_warehouse = "Envases IB Llenos - LSSA"

    if "Envases IB" in sed.t_warehouse:
        target = STOCK
        move["to_stock"] = sed.t_warehouse
        move["to_customer"] = None
    else:
        target = CUST
        move["to_stock"] = None
        move["to_customer"] = sed.t_warehouse
        move["if_customer"] = sed.t_warehouse

    move["direction"] = f"{source} >> {target}"
    move["timestamp"] = f"{sed.posting_date} {sed.posting_time}"
    move["bapu_id"] = f"{sed.name}"
    # print(move)

    moves = []
    for sn in sed.serial_no.split("\n"):
        returnable = { 
            "doctype": 'Returnable Movement',
            "parenttype": 'Returnable',
            "parent": sn 
        }
        returnable.update(move)
        moves.append(returnable)
        # print(returnable)

    return moves

qryWhses = f"""
    select distinct M.if_customer
      from `tabReturnable Movement` M left join `tabWarehouse` W 
        on M.if_customer = W.name
     where M.if_customer is not null
       and W.name is null
    ;
"""

def createAllMissingWarehouses():
    print(f"Creating all missing warehouses")
    missingWarehouses = frappe.db.sql(qryWhses)
    for missingWarehouse in missingWarehouses:
        print(missingWarehouse[0])
        whse = frappe.get_doc({
                     'doctype': 'Warehouse',
                        'name': missingWarehouse[0],
                   'docstatus': 1,
              'warehouse_name': missingWarehouse[0],
              'warehouse_type': 'Consignado',
            'parent_warehouse': 'Envases IB Custodia del Cliente - LSSA',
                    'is_group': 0,
                     'account': '1.1.5.06 - Envases Custodiados - LSSA',
                     'company': 'Logichem Solutions S. A.'
        })
        print(whse)
        whse.insert()

    frappe.db.commit()

    print(f"Done creating all missing warehouses.\n")

def getLastCustomer(serial_no):
    abbr = frappe.db.sql(f"""select abbr from `tabCompany` where name like '%Logichem%'""")[0][0]
    # print(f"abbr :: {abbr}")
    qry = f"""
        select REPLACE(if_customer, concat(' - ', '{abbr}'), '')
          from `tabReturnable Movement`
         where parent = '{serial_no}'
           and if_customer is not null
      order by idx asc
         limit 1
    """ 
    return frappe.db.sql(qry)[0][0]

def getReturnableState(move, returnable):
    print(f"""

                    getReturnableState()
{move.to_stock}
{move.to_customer}
        """)
    if returnable.last_customer == "Envases IB Rotos - LSSA":
        return "Roto"
    if returnable.coherente != "Si":
        return "Confuso"
    if move.to_stock == "Envases IB Sucios - LSSA":
        return "Sucio"
    if move.to_stock == "Envases IB Llenos - LSSA":
        return "Lleno"
    return "Donde Cliente"

def zeroThePurchaseRateOfAllFichas():
    data = frappe.db.sql("""
        UPDATE `tabSerial No`
           SET purchase_rate = 0.00
         WHERE item_code = 'FICHA - para envase IB de 5GL'
    """, as_dict = 1)

    return data

@frappe.whitelist()
def returnableMoveFromMaterialTransfer():

    f = open("/dev/shm/returnableMovesCron.log", "a")
    msg = f"""\n\n\nStarting :: returnableMoveFromMaterialTransfer()"""

    zeroThePurchaseRateOfAllFichas()

    createAllMissingWarehouses()

    print(msg)
    stockEntryDetails = getOneStockEntry()

    msg = "returnableMoveFromMaterialTransfer()"
    if stockEntryDetails:

        entry = stockEntryDetails[0].name
        msg = f"{datetime.datetime.now()} Stock Entry: {entry}"
        print(msg)

        movements = []
        sep = ""
        msg = f" {msg} => "

        for stockEntryDetail in stockEntryDetails:
            
            movements.extend(reformatStockEntryDetail(stockEntryDetail))

        for movement in movements:
            # print(f"movement ---------------------------------------------------------")
            # print(movement)
            # print(f"movement => {movement['parent']}   {movement['direction']}   {movement['if_customer']}")
            msg = f"{msg}{sep}{movement['parent']}"
            sep = ", "

            move = frappe.get_doc(movement)
            print(f"Ready to insert movement: | {move.parent} | {move.direction} | {move.if_customer} | {move.from_customer}")

            # if move.direction == "Cust >> Stock" and move.from_customer == "Cuarto Limpio - LSSA" and move.to_stock == "Envases IB Llenos - LSSA":
            #     print("!!!!!!!!!!!!!!!!")

            if move.if_customer is None:
                whse = frappe.get_doc("Warehouse", move.to_stock)
            else:
                whse = frappe.get_doc("Warehouse", move.if_customer)
            # print(whse)
            move.insert()
            frappe.db.commit()

            # print("Ready to increment movement indexes:")
            incr = incrementReturnableMovementIndexes(movement["parent"])
            # print(incr)
            frappe.db.sql(incr)

            totalMoves= getReturnableMoveCount(move.parent)

            totalDepartures = getReturnableDeparturesCount(move.parent)
            totalArrivals = getReturnableArrivalsCount(move.parent)
            totalFillings = getReturnableFillingsCount(move.parent)
            coherente = "Si"
            if totalDepartures >= totalArrivals:
                if totalFillings < totalDepartures:
                    coherente = "Más salidas que rellenos !"
                if totalFillings > totalDepartures + 1:
                    coherente = "Más rellenos que salidas !"
            elif totalDepartures > totalArrivals + 2:
                    coherente = "Las salidas superan las llegadas !"
            elif totalDepartures < totalArrivals:
                    coherente = " Las llegadas superan las salidas !"

            returnable = frappe.get_doc("Returnable", move.parent)
            # print(f"Returnable : {returnable.name}")

            returnable.fills = totalFillings
            # returnable.last_customer = getLastCustomer(move.parent)
            returnable.times_out = totalDepartures
            returnable.times_in = totalArrivals
            returnable.coherente = coherente
            
            returnable.last_customer = getLastCustomer(move.parent)

            returnable.state = getReturnableState(move, returnable)


            # print(returnable.coherente)
            returnable.save()

            frappe.db.commit()
            # print(f"Finished  {move.parent}\n....")

            print(f" - Processed returnable :: {returnable.name}")

        f.write(f"{msg}\n")
    print(f"Finished :: {msg}")

    f.close()


def startStockEntry(self, method):
    deliveryNote = self
    print("""#    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    """)
    print("""#    #    {}   """.format(method))
    deliveryNoteItems = deliveryNote.items
    for item in deliveryNoteItems:
        print("""#    #    {}   """.format(
            item.item_code,
            item.description
        ))

 # 1) Edit Returnable Movement doctype
 #   1a) Fix Naming Series
 #    - Type: select
 #    - Name: naming_series
 #    - Options: "RET-MOV-.#########"
 #    - Set Only Once: True 
 #    - No Copy: True 
 #    - Print Hide: True 
 #    - Label: Naming Series
 #   1b) Customers must be Warehouses
 
 # 2) Run FixNamingSeries.sh
 #    - cd ~/frappe-bench-DERPLS/apps/returnable/returnable/returnable/doctype/returnable_movement
 #      ./FixNamingSeries.sh
 
 # 3) Reverse the order of Movements
 #   ALTER TABLE `tabReturnable Movement` ADD INDEX ret_idx (parent, idx);
 #   describe update `tabReturnable Movement` A set idx = (select max(idx) from `tabReturnable Movement` B where A.parent = B.parent) - idx + 1; # where A.parent in ("IBAA038", "IBAA049");
 #   update `tabReturnable Movement` A set idx = (select max(idx) from `tabReturnable Movement` B where A.parent = B.parent) - idx + 1; # where A.parent in ("IBAA038", "IBAA049");
 
 # 4) Change Customers to Warehouses


