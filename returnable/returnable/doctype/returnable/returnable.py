# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

import os
import errno
# import time

from frappe.model.document import Document

NAME_COMPANY = ""
ABBR_COMPANY = ""
FULL_COMPANY = ""
SUCIOS = ""
LLENOS = ""
ROTOS = ""
ERRORS = ""
EXISTING_LOCATIONS = ""

LOG_DIR = "/dev/shm/erpnext"


def prepareGlobals(company):
    global NAME_COMPANY
    global ABBR_COMPANY
    global FULL_COMPANY
    global SUCIOS
    global LLENOS
    global ROTOS
    global ERRORS
    global EXISTING_LOCATIONS

    theCompany = frappe.get_doc('Company', company)
    NAME_COMPANY = theCompany.company_name
    ABBR_COMPANY = theCompany.abbr
    FULL_COMPANY = "{} - {}".format(NAME_COMPANY, ABBR_COMPANY)

    SUCIOS = "Envases IB Sucios - {}".format(ABBR_COMPANY)
    LLENOS = "Envases IB Llenos - {}".format(ABBR_COMPANY)
    ROTOS = "Envases IB Rotos - {}".format(ABBR_COMPANY)
    ERRORS = "Envases Con Error"

    EXISTING_LOCATIONS = set({SUCIOS, LLENOS, ROTOS})


def prepareTemporaryTables():
    LG("\nDropping `tabLast Batches`")
    frappe.db.sql("""DROP TABLE IF EXISTS `tabLast Batches`""", as_dict=0)

    LG("Creating `tabLast Batches`")
    frappe.db.sql("""CREATE TABLE `tabLast Batches`
                        SELECT   I.Bottle
                               , B.name AS batch
                               , B.direction
                               , B.bapu_id
                               , B.timestamp
                          FROM `tabReturnable Batch` B, `tabReturnable Batch Item` I
                         WHERE I.parent = B.name
                           AND I.name in (
                                SELECT max(J.name) AS name
                                  FROM `tabReturnable Batch` C, `tabReturnable Batch Item` J
                                 WHERE J.parent = C.name
                              GROUP BY J.Bottle
                            )
                      ORDER BY Bottle""", as_dict=0)
    LG("Created `tabLast Batches`")

    LG("\nDropping `tabLast Moves`")
    frappe.db.sql("""DROP TABLE IF EXISTS `tabLast Moves`""", as_dict=0)

    LG("Creating `tabLast Moves`")
    frappe.db.sql("""  CREATE TABLE `tabLast Moves`
                        SELECT
                               M.parent as Bottle
                             , M.name AS Move
                             , M.direction AS Direction
                             , M.if_customer AS last_customer
                             , M.bapu_id
                             , M.timestamp AS Last
                             , CASE M.direction
                                 WHEN 'Cust >> Stock' THEN 'Sucio'
                                 WHEN 'Stock >> Stock' THEN 'Lleno'
                                 ELSE 'Donde Cliente'
                               END AS state
                          FROM `tabReturnable Movement` M
                         WHERE
                             M.name IN (
                                    SELECT
                                          MAX(N.name) AS name
                                     FROM  `tabReturnable Movement` N
                                    WHERE N.parent like 'IB%'
                                 GROUP BY N.parent
                            )
                      ORDER BY M.parent""", as_dict=0)
    LG("Created `tabLast Moves`")

    frappe.db.commit()


def LG(txt, end="\n", logname="{}/result.log".format(LOG_DIR)):
    # logname = "/dev/shm/erpnext/result.log"
    if os.path.exists(logname):
        append_write = 'a'  # append if already exists
    else:
        try:
            if not os.path.exists(LOG_DIR):
                os.makedirs(LOG_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        append_write = 'w'  # make a new file if not

    logfile = open(logname, append_write)
    logfile.write(txt + end)
    logfile.close()


class Returnable(Document):
    pass


def getQryReturnable(returnable='%', state='%', offset=0, rows=0):
    limit = "" if offset + rows == 0 else "LIMIT {}, {}".format(offset, rows)
    return """
            SELECT Bottle
                 , state
                 , last_customer
                 , bapu_id
                 , Last
          FROM `tabLast Moves`
             WHERE Bottle LIKE '{0}'
               AND state LIKE '{1}'
          ORDER BY last_customer
           {2}
    """.format(returnable, state, limit)

# def getQryReturnable(returnable='%', state='%', offset=0, rows=0):
#     limit = "" if offset + rows == 0 else "LIMIT {}, {}".format(offset, rows)
#     return """
#             SELECT *
#                 FROM `tabReturnable` R
#              WHERE name LIKE '{0}'
#                  AND state LIKE '{1}'
#                  AND last_customer not like 'Abner Victor%'
#         ORDER BY last_customer
#              {2}
#              ;
#     """.format(returnable, state, limit)


def createStockEntry(spec):
    # LG("Create {} item stock entry to {}.".format(
    #                   len(spec.serial_numbers), spec.warehouse_name))
    stock_entry = frappe.get_doc({
        'doctype': 'Stock Entry',
        'docstatus': 0,
        "set_posting_time": 1,
        "posting_date": spec.timestamp.strftime('%Y/%m/%d'),
        "posting_time": spec.timestamp.strftime('%I:%M:%S'),
        'to_warehouse': spec.warehouse_name,
        'stock_entry_type': 'Material Receipt'
    })

    LG("-----")

    stock_entry.append('items', {
        'qty': len(spec.serial_numbers),
        'item_code': 'Envase de 5GL Iridium Blue',
        'serial_no': ",".join(spec.serial_numbers)
    })

    stock_entry.save()
    stock_entry.submit()

    LG("Commit: {}".format(spec.warehouse_name))
    frappe.db.commit()


def createReturnablesStockEntries(list, name):
    numbers = []
    for returnable in list:
        LG("{} : '{}'".format(name, returnable.Bottle))
        numbers.append(returnable.Bottle)

    LG("Create Stock Entry for : {}".format(numbers))
    createStockEntry(frappe._dict(
        {'serial_numbers': numbers, 'warehouse_name': name, 'timestamp': returnable.Last}
    ))


def processDirty(list):
    createReturnablesStockEntries(list, SUCIOS)


def processFull(list):
    createReturnablesStockEntries(list, LLENOS)


def createBatchedStockEntries():
    LG("\n----- 1")
    qryBatches = """SELECT DISTINCT
                  B.timestamp
                , COUNT(B.Bottle) as bottles
                , B.bapu_id
          FROM  `tabLast Batches` B
              , `tabLast Moves` M
         WHERE B.Bottle = M.Bottle
           AND B.direction = M.direction
           AND B.direction = "Stock >> Stock"
           AND B.timestamp > '2017-03-06 12:00:00'
         GROUP BY B.bapu_id
         ORDER BY B.timestamp
    """

    LG("----- 2")
    batches = frappe.db.sql(qryBatches, as_dict=True)
    LG("----- 3")
    for batch in batches:
        date = batch.timestamp.strftime('%Y/%m/%d')
        time = batch.timestamp.strftime('%I:%M:%S')
        LG("Batch id: '{}', Date: '{}', Time: '{}', Bottle: '{}'".format(
            batch.bapu_id, date, time, batch.bottles))

        LG("----- 4")
        try:
            docBatch = frappe.get_doc({
                "doctype": 'Batch',
                "docstatus": 1,
                "item": "Agua IridiumbLue",
                "manufacturing_date": date,
                "batch_qty": batch.bottles,
                "batch_id": batch.bapu_id,
                "reference_doctype": "Stock Entry"
            })

            docBatch.save()
            docBatch.submit()

            LG("Commit: {}".format(docBatch.batch_id))
            frappe.db.commit()

            LG("\n----- A")
            stock_entry = frappe.get_doc({
                'doctype': 'Stock Entry',
                'docstatus': 0,
                'to_warehouse': LLENOS,
                'stock_entry_type': 'Material Receipt'
            })

            stock_entry.append('items', {
                "qty": batch.bottles,
                "batch_no": batch.bapu_id,
                "item_code": "Agua IridiumbLue"
            })

            stock_entry.save()
            stock_entry.submit()

            LG("Commit : {}".format(batch.bapu_id))
            frappe.db.commit()

        except Exception as e:
            LG("Err {}".format(e))


def processReturnable(returnable):
    LG("Returnable ==> {}.  State {}.  Last cust {}.".format(
        returnable.name, returnable.state, returnable.last_customer
    ))


def createStockEntryForCustomer(returnable, numbers):
    # LG("Create {} item stock entry for customer :: {}.  ({})".format(
    #                    len(numbers), returnable.last_customer, NAME_COMPANY))

    whs_name = "{} - {}".format(returnable.last_customer, ABBR_COMPANY)
    ccw = frappe.get_doc('Warehouse', whs_name)

    LG("Creating '{}' item Stock Entry for {}".format(numbers, ccw.name))
    createStockEntry(frappe._dict({
        'serial_numbers': numbers,
        'warehouse_name': ccw.name,
        'timestamp': returnable.Last
    }))


def processByCustomer(list):

    LG("\n")
    # LG("By customer : {}".format(len(list)))
    customer = ''
    numbers = []
    previousReturnable = {}

    for returnable in list:
        if customer == returnable.last_customer or customer == '':
            numbers.append(returnable.Bottle)
        else:
            createStockEntryForCustomer(previousReturnable, numbers)
            numbers.clear()
            numbers.append(returnable.Bottle)

        customer = returnable.last_customer
        previousReturnable = returnable
        # processReturnable(returnable)
    if any(previousReturnable):
        LG("Doing Last One")
        createStockEntryForCustomer(previousReturnable, numbers)

    LG("Completed block")


def makeWarehouses(list):
    LG("\n")
    for returnable in list:

        whs_name = "{} - {}".format(returnable.last_customer, ABBR_COMPANY)
        # LG("Check if warehouse '{}' exists".format(whs_name))
        try:
            frappe.get_doc('Warehouse', whs_name)
        except:  # noqa
            LG("Creating warehouse '{}'.".format(whs_name))
            customer_consignment_warehouse = frappe.get_doc({
                'doctype': 'Warehouse',
                'warehouse_name': returnable.last_customer,
                'parent_warehouse': "{} - {}".format(
                    'Envases IB Custodia del Cliente', ABBR_COMPANY),
                'company': NAME_COMPANY,
                'account': "{} - {}".format(
                    '1.1.5.06 - Envases Custodiados', ABBR_COMPANY),
                'warehouse_type': 'Consignado'
            })

            customer_consignment_warehouse.save()
            customer_consignment_warehouse.submit()
            LG("- o 0 o -")


def processReturnables(query, func):
    returnables = frappe.db.sql(query, as_dict=True)
    LG("Returnables {}\n".format(returnables))
    func(returnables)
    return len(returnables)


def processReturnablesGroup(group, func):
    LG("Process Returnables Group...")
    rows = cnt = 50
    offset = 0
    # sleep = 2  # seconds
    while cnt == rows:
        query = getQryReturnable(returnable='IB%', state=group, rows=rows, offset=offset)
        # LG("query {}\n".format(query))
        cnt = processReturnables(query, func)
        offset = offset + rows
        LG("\n* Row count {}\n".format(cnt))
        # time.sleep(2)


def install_returnables(company):
    LG("Getting values for company :: {}".format(company))
    prepareGlobals(company)

    prepareTemporaryTables()

    LG("\n\nCreate {} customer consignment warehouses.".format(NAME_COMPANY))
    processReturnablesGroup('Donde Cliente', makeWarehouses)

    LG("\n\nProcess Customer Returnables")
    processReturnablesGroup('Donde Cliente', processByCustomer)

    LG("\n\nProcess Dirty Returnables ")
    processReturnablesGroup('Sucio', processDirty)

    LG("\n\nProcess Full Returnables")
    processReturnablesGroup('Lleno', processFull)

    LG("\n\nProcess Batches")
    createBatchedStockEntries()

    LG("Completed all blocks")

    return "Installed Returnables"


@frappe.whitelist()
def se_count(company):
    prepareGlobals(company)

    data = frappe.db.sql("""SELECT count(*) FROM `tabStock Entry` se""", as_dict=0)
    cnt = data[0][0]
    # LG("-- {}".format(cnt), logname = "{}/notification.log".format(LOG_DIR))

    LG("{}".format(cnt), logname="{}/notification.log".format(LOG_DIR))
    LG("-- {}  | ".format(cnt))

    return "{} Stock Entries".format(cnt)


@frappe.whitelist()
def tester(company):
    LG("Getting values for company :: {}".format(company))
    prepareGlobals(company)

    prepareTemporaryTables()

    bottle = "IBEE089"  # -------------------------

    LG("\nQuerying `tabLast Batches`")
    batchesByBottle = frappe.db.sql("""
        SELECT Bottle, batch, bapu_id, timestamp
          FROM `tabLast Batches`
        """, as_dict=1)

    luBottle = {}
    for batchBottle in batchesByBottle:
        # LG("Bottle: {}".format(batchBottle.Bottle))
        luBottle[batchBottle.Bottle] = {
            "batch": batchBottle.batch,
            "timestamp": batchBottle.timestamp,
            "bapu_id": batchBottle.bapu_id
        }

    LG("Bottle: {} Batch: {} ".format(bottle, luBottle[bottle]))

    LG("\nQuerying `tabLast Moves`")
    movesByBottle = frappe.db.sql("""
        SELECT Bottle, state, last_customer, bapu_id, Last
          FROM `tabLast Moves`
        """, as_dict=1)

    # LIMIT 10""", as_dict=1)

    # LG("Move: {} ".format(movesByBottle))

    luMove = {}
    for bottleMoves in movesByBottle:
        luMove[bottleMoves.Bottle] = {
            "batch": bottleMoves.state,
            "last_customer": bottleMoves.last_customer,
            "bapu_id": bottleMoves.bapu_id,
            "timestamp": bottleMoves.Last
        }

    LG("Bottle: {} State: {} ".format(bottle, luMove[bottle]))

    # LG("Queried `tabLast Batches`")

    return "Test Complete"


@frappe.whitelist()
def installReturnables(company):
    return install_returnables(company)


@frappe.whitelist()
def queueInstallReturnables(company):
    frappe.enqueue(
        'returnable.returnable.doctype.returnable.returnable.install_returnables',
        company=company, is_async=True, timeout=240000)
    return "Enqueued"
