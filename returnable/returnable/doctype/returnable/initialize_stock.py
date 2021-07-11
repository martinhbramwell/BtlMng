# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

import os
import errno
import requests, time, datetime
import json
import re

from datetime import datetime
from pathlib import Path
from time import sleep

from frappe.model.document import Document

NAME_COMPANY = ""
ABBR_COMPANY = ""
FULL_COMPANY = ""

SUCIOS = ""
LLENOS = ""
ROTOS = ""
ALERTAR = ""
PERDIDOS = ""

EXISTING_LOCATIONS = ""

LOG_DIR = "/dev/shm/erpnext"

BAPU_EP = 'http://www.iridiumblue.ec/erp/bapu/test/php/envases/envases_all_datatables.php'

def prepareGlobals(company):
    global NAME_COMPANY
    global ABBR_COMPANY
    global FULL_COMPANY
    global SUCIOS
    global LLENOS
    global ROTOS
    global ALERTAR
    global PERDIDOS
    global EXISTING_LOCATIONS

    theCompany = frappe.get_doc('Company', company)
    NAME_COMPANY = theCompany.company_name
    ABBR_COMPANY = theCompany.abbr
    FULL_COMPANY = "{} - {}".format(NAME_COMPANY, ABBR_COMPANY)

    SUCIOS = "Envases IB Sucios - {}".format(ABBR_COMPANY)
    LLENOS = "Envases IB Llenos - {}".format(ABBR_COMPANY)
    ROTOS = "Envases IB Rotos - {}".format(ABBR_COMPANY)
    ALERTAR = "Envases IB ALERTAR - {}".format(ABBR_COMPANY)
    PERDIDOS = "Envases IB Perdidos - {}".format(ABBR_COMPANY)

    EXISTING_LOCATIONS = set({SUCIOS, LLENOS, ROTOS, ALERTAR, PERDIDOS})


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


def createStockEntry(spec):
    # LG("Create {} item stock entry to {}.".format(
    #                   len(spec.serial_numbers), spec.warehouse_name))
    body = {
      "doctype": "Stock Entry",
      "docstatus": 0,
      "stock_entry_type": "Material Transfer",
      "title": "Move {}xx to {}".format(spec.sn_block, spec.tgt),
      "items": [
        {
          "qty": spec.qty,
          "item_code": "Envase de 5GL Iridium Blue",
          "s_warehouse": spec.src,
          "t_warehouse": spec.tgt,
          "serial_no": spec.serial_no
        }
      ]
    }

    print("----- {}".format(body))

    stock_entry = frappe.get_doc(body)

    stock_entry.save()
    stock_entry.submit()

    LG("Commit: {}".format(spec.warehouse_name))
    frappe.db.commit()

def makeWarehouse(name, parent_warehouse='Envases IB Custodia del Cliente', account='1.1.5.06 - Envases Custodiados'):
    whs_name = "{} - {}".format(name, ABBR_COMPANY)
    parent_whs = "{} - {}".format(parent_warehouse, ABBR_COMPANY)
    acct = "{} - {}".format(account, ABBR_COMPANY)
    LG("Check if warehouse '{}' exists".format(whs_name))
    try:
        frappe.get_doc('Warehouse', whs_name)
    except:  # noqa
        LG("Creating warehouse '{}'.".format(whs_name))
        customer_consignment_warehouse = frappe.get_doc({
            'doctype': 'Warehouse',
            'warehouse_name': name,
            'parent_warehouse': parent_whs,
            'company': NAME_COMPANY,
            'account': acct,
            'warehouse_type': 'Consignado'
        })

        customer_consignment_warehouse.save()
        customer_consignment_warehouse.submit()

        frappe.db.commit()
        print("Committed : {}".format(whs_name))

    return whs_name

def pseudoDate(Ymd_HM, day_num, with_date, with_time):
    day_str = str(day_num).zfill(2)
    day = datetime.strptime(Ymd_HM.format(day_str), "%Y-%m-%d %H:%M")
    dtFmt = ''
    if with_date:
        dtFmt = '%Y-%m-%d'
    if with_time:
        if len(dtFmt) > 0:
            dtFmt = "{} ".format(dtFmt)
        dtFmt = "{}{}".format(dtFmt, '%H:%M:%S')

    return day.strftime(dtFmt)

def getBadDataLookupDict():
    fixLookUp = frappe._dict()
    corrections = open('/opt/docTypeHandlers/correctBadData.json', 'r')
    for correction in json.load(corrections):
        # print(correction['PAT'])
        fixLookUp[correction['PAT']] = correction['FIX']
    corrections.close()
    return fixLookUp

def getBAPUCookie():
    cookie = ""
    envars = Path("{}/../apps/returnable/envars.sh".format(os.getcwd())).resolve()
    with open(envars, 'r') as input:
       for line in input:
           if 'COOKIE_VAL' in line:
                parts = re.search('COOKIE_VAL="(.+?)";', line)
                if parts:
                    cookie = parts.group(1)
                break

    return cookie

def getBottlesStatusFromBAPU(cookie):
    response = requests.get(BAPU_EP, headers={"Cookie": "PHPSESSID={}".format(cookie)})
    print('.................  ::::   ==|==   ::::  ..................')
    time.sleep(2)
    bottleList = response.json()
    return bottleList['aaData']

def prepareReferenceTables(bottlesStatusPage):
    fixLookUp = getBadDataLookupDict()

    customers = frappe._dict()
    bottle_blocks = frappe._dict()
    for bottle in bottlesStatusPage:
        if bottle[1][0:2] == "CL":
            bottle_group = "CLXX0"
        else:
            bottle_group = "{}0".format(bottle[1][0:4]) if int(bottle[1][4:5]) < 5 else "{}5".format(bottle[1][0:4])
        bottle_blocks.setdefault(bottle_group, []).append(bottle)
        if bottle[3] == 'cliente':
            cust = bottle[6]
            if len(cust) < 1 or int(bottle[4]) + int(bottle[5]) < 1:
                cust = 'Envases Perdidos'
                bottle[6] = cust
            # cust = 'Envases Perdidos' if len(bottle[6]) < 1 else bottle[6]
            cust = cust if cust not in fixLookUp.keys() else fixLookUp[cust]
            customers.setdefault(cust, []).append(bottle)

    return customers, bottle_blocks

    # [
    #   "1",
    #   "IBAA001",
    #   "A",
    #   "cliente",
    #   "5",
    #   "4",
    #   "LEVO CIA LTDA"
    # ],


def createPurchaseOrder(spec):
    purchase_order = frappe.get_doc({
        "doctype": 'Purchase Order',
        "docstatus": 0,
        "supplier": spec.supplier,
        "creation": spec.creation,
        "transaction_date": spec.transaction_date,
        "schedule_date": spec.schedule_date,
        "order_confirmation_no": spec.order_confirmation_no,
        "docstatus": 1,
        "items": [{
            "item_code": "Envase de 5GL Iridium Blue",
            "qty": spec.quantity,
            "rate": 8.04,
            "warehouse": "Envases IB Sucios - LSSA"
        }]
    })

    LG("-----")

    purchase_order.save()
    purchase_order.submit()

    LG("Commit: {}".format(spec.warehouse_name))
    frappe.db.commit()

    return purchase_order

def createPurchaseReceipt(spec):
    body = {
        'doctype': 'Purchase Receipt',
        "creation": spec.creation,
        'docstatus': 0,
        'naming_series': 'MAT-PRE-.YYYY.-',
        'set_posting_time': 1,
        'posting_date': spec.posting_date,
        'posting_time': spec.posting_time,
        'supplier': spec.supplier,
        'set_warehouse': 'Envases IB Sucios - LSSA',
        'total_qty': spec.quantity,
        'items': [{
            'docstatus': 0,
            'item_code': 'Envase de 5GL Iridium Blue',
            'qty': spec.quantity,
            "rate": 8.04,
            'received_stock_qty': spec.quantity,
            'warehouse': 'Envases IB Sucios - LSSA',
            'purchase_order': spec.purchase_order,
            'purchase_order_item': spec.purchase_order_item,
            'schedule_date': spec.schedule_date,
            'serial_no': spec.serial_no,
            'include_exploded_items': 0,
            'expense_account': '5.1.1.03 - Costos Sobre Ventas - LSSA'
        }]
    }

    print(body)
    purchase_receipt = frappe.get_doc(body)

    LG("-----")

    purchase_receipt.save()
    purchase_receipt.submit()

    LG("Commit: {}".format(spec.purchase_order))
    frappe.db.commit()

    return purchase_receipt

def generatePurchaseOrders(bottle_blocks):
    purchase_orders = frappe._dict()
    idx = 0
    for block_id in bottle_blocks.keys():
        idx += 1
        item_count = len(bottle_blocks[block_id])

        creation = pseudoDate("2015-12-{} 15:52", idx, True, True)
        xaction = pseudoDate("2015-12-{} 15:52", idx, True, False)
        scheduled = pseudoDate("2016-01-{} 15:52", idx, True, False)
        print("{} has {} entries. Created: {} Transaction: {} Scheduled: {}".format(block_id, item_count, creation, xaction, scheduled))

        purchase_order = frappe._dict()
        purchase_order['serial_numbers'] = bottle_blocks[block_id]

        purchase_order['po'] = createPurchaseOrder(frappe._dict({
            'supplier': "Fabrica De Envases S. A. FADESA",
            'order_confirmation_no': block_id,
            'creation': creation,
            'transaction_date': xaction,
            'schedule_date': scheduled,
            'quantity': item_count
        }))

        purchase_orders.setdefault(block_id, purchase_order)

    return purchase_orders

def generatePurchaseReceipts(serial_number_blocks):
    all_purchase_orders = frappe.db.get_list('Purchase Order')

    purchase_receipts = frappe._dict()
    for po in all_purchase_orders:
        purchase_receipt = frappe._dict()
        PurchaseOrder = frappe.get_doc('Purchase Order', po.name)
        po_seq = int(PurchaseOrder.name[13:18])
        if po_seq != 88:
            creation = pseudoDate("2016-01-{} 15:52", po_seq, True, True)
            posting_date = pseudoDate("2016-01-{} 16:59", po_seq, True, False)
            posting_time = pseudoDate("2016-01-{} 16:59", po_seq, False, True)
            supplier = "Fabrica De Envases S. A. FADESA"

            purchase_order = PurchaseOrder.name
            purchase_order_item = PurchaseOrder.items[0].name
            scheduled = pseudoDate("2016-01-{} 16:59", po_seq, True, False)

            block_id = PurchaseOrder.order_confirmation_no
            quantity = serial_number_blocks[block_id].qty
            serial_no = serial_number_blocks[block_id].sns

            print("PO #{}: {}/{} matched with {} having {} bottles".format(str(po_seq).zfill(2), purchase_order, purchase_order_item, block_id, quantity))
            print( "Creation: {}. Posting Date: {},  Time: {}.  Scheduled: {}".format(creation, posting_date, posting_time, scheduled))

            purchase_receipt['pr'] = createPurchaseReceipt(frappe._dict({
            # createPurchaseReceipt(frappe._dict({
                'creation': creation,
                'posting_date': posting_date,
                'posting_time': posting_time,
                'supplier': supplier,
                'purchase_order': purchase_order,
                'purchase_order_item': purchase_order_item,
                'schedule_date': scheduled,
                'quantity': quantity,
                'serial_no': serial_no
            }))

        # purchase_receipts.setdefault(block_id, purchase_receipt)

def getSerialNumbers(bottle_blocks):
    serial_number_blocks = frappe._dict()
    for block_id in bottle_blocks.keys():
        serial_numbers = frappe._dict()
        serial_no = []

        perdidos = []
        alertar = []
        rotos = []
        sucios = []
        llenos = []
        cliente = []
        # if block_id == "CLXX0":
        for bottle in bottle_blocks[block_id]:
            # print("==== Block: {} ==> {}".format(block_id, bottle))
            serial_no.append(bottle[1])
            if int(bottle[4]) + int(bottle[5]) < 1:
                # print("\nEnvases Perdidos: {} ==> {}".format(bottle[1], bottle[3]))
                perdidos.append(bottle[1])
                continue

            if bottle[6] == 'Envases Perdidos':
                # print("\nEnvases Perdidos: {} ==> {}".format(bottle[1], bottle[3]))
                perdidos.append(bottle[1])
                continue

            if bottle[6] == 'ALERTAR':
                # print("\nALERTAR: {} ==> {}".format(bottle[1], bottle[3]))
                alertar.append(bottle[1])
                continue

            if bottle[3] == 'error':
                # print("\nALERTAR: {} ==> {}".format(bottle[1], bottle[3]))
                alertar.append(bottle[1])
                continue

            if bottle[6] == 'Envases Rotos':
                # print("\nEnvases Rotos: {} ==> {}".format(bottle[1], bottle[3]))
                rotos.append(bottle[1])
                continue

            if bottle[3] == 'vacio':
                # print("\nEnvases Sucios: {} ==> {}".format(bottle[1], bottle[3]))
                sucios.append(bottle[1])
                continue

            if bottle[3] == 'lleno':
                # print("\nEnvases Sucios: {} ==> {}".format(bottle[1], bottle[3]))
                llenos.append(bottle[1])
                continue

            if bottle[3] == 'cliente':
                # print("\nConsignado: {} ==> {}".format(bottle[1], bottle[3]))
                cliente.append(bottle[1])
                continue

        # ['3086', 'IBEE089', 'A', 'cliente', '18', '17', 'Iridium Blue (Venta No Registrada)']

        serial_numbers["sns"] = ", ".join(serial_no)

        serial_numbers[PERDIDOS] = perdidos
        serial_numbers[ALERTAR] = alertar
        serial_numbers[ROTOS] = rotos
        serial_numbers[SUCIOS] = sucios
        serial_numbers[LLENOS] = llenos

        serial_numbers["cliente"] = cliente

        serial_numbers["qty"] = len(serial_no)

        serial_number_blocks[block_id] = serial_numbers

    return serial_number_blocks

def transferBottles(target, serial_number_blocks):
    for block_id in serial_number_blocks:
        bottles = serial_number_blocks[block_id][target]
        qty = len(bottles)
        if qty > 0:
            print("Transferring {} ({}) to {}".format(block_id, qty, target))

            spec = frappe._dict({
                'sn_block': block_id,
                'qty': qty,
                'src': SUCIOS,
                'tgt': target,
                'serial_no': ", ".join(bottles)
            })

            print("Spec: {}".format(spec))
            createStockEntry(spec)

        sleep(2)


def updateSerialNumbersWithReceiptNumber(serial_number_blocks):
    all_purchase_orders = frappe.db.get_list('Purchase Order')
    for purchase_order in all_purchase_orders:
        po = frappe.get_doc('Purchase Order', purchase_order)
        block_id = po.order_confirmation_no
        print("{} ==> {}".format(po.name, block_id))
        sns = serial_number_blocks[block_id].sns
        first = sns.split()[0].rstrip(",")
        last = sns.split()[-1]

        # print("{} -- >{}< | >{}<".format(block_id, first, last))

        values = {'first': first, 'last': last, 'po_no': po.name}
        data = frappe.db.sql("""
            UPDATE `tabSerial No` tsn
            SET purchase_document_no = %(po_no)s
            WHERE name between %(first)s and %(last)s
        """, values=values, as_dict=0)

        data = frappe.db.sql("""
            SELECT name, warehouse, purchase_document_no
            FROM `tabSerial No` tsn
            WHERE name between %(first)s and %(last)s
        """, values=values, as_dict=0)

        frappe.db.commit()
        # print("Block: {} => {}".format(block_id, data))

    # for block_id in bottle_blocks:
    #     print("Block {} ==> {}".format(block_id, bottle_blocks[block_id]))

@frappe.whitelist()
def tester(company):
    LG("Getting values for company :: {}".format(company))
    prepareGlobals(company)

    makeWarehouse("Envases IB Perdidos", parent_warehouse='Envases Iridium Blue', account='5.1.1.06 - Ajuste De Existencias')
    makeWarehouse("Envases IB ALERTAR", parent_warehouse='Envases Iridium Blue', account='5.1.1.06 - Ajuste De Existencias')

    bottlesStatusPage = getBottlesStatusFromBAPU(getBAPUCookie())
    print(' *** *** *** ***  ', BAPU_EP, ' |<>|  Got', len(bottlesStatusPage), 'bottles.  *** *** *** *** *** ');

    customers, bottle_blocks = prepareReferenceTables(bottlesStatusPage)

    serial_number_blocks = getSerialNumbers(bottle_blocks)

    # generatePurchaseOrders(bottle_blocks)

    # generatePurchaseReceipts(serial_number_blocks)

    # updateSerialNumbersWithReceiptNumber(serial_number_blocks)

    # locations = [PERDIDOS, ALERTAR, ROTOS, LLENOS]
    # for location in locations:
    #     transferBottles(location, serial_number_blocks)

    for customer_name in sorted(customers.keys()):
        if customer_name not in [ "ALERTAR", "Envases Rotos", "Envases Perdidos", "Luca Galeotti" ]:
            location = makeWarehouse(customer_name.strip())
            print("New stock location: >{}<".format(location))

    frappe.db.commit()
    sleep(5)

    print("\n\nReady to move bottles to customers...")

    for customer_name in sorted(customers.keys()):
        if customer_name not in [ "ALERTAR", "Envases Rotos", "Envases Perdidos", "Luca Galeotti" ]:
            item_count = len(customers[customer_name])
            customer = frappe.get_doc('Customer', customer_name)
            print("{} ({}) has {} entries.".format(customer_name, customer.gender, item_count))
            bottles = []
            for bottle_block in customers[customer_name]:
                bottles.append(bottle_block[1])
                print("    Bottles {}.".format(bottles))
                # print("    Bottles {}.".format(bottle_block))

            qty = len(bottles)
            if qty > 0:
                location = "{} - {}".format(customer_name.strip(), ABBR_COMPANY)
                body = {
                  "doctype": "Stock Entry",
                  "docstatus": 0,
                  "stock_entry_type": "Material Transfer",
                  "title": "Move {} bottles to {}".format(qty, location),
                  "items": [
                    {
                      "qty": qty,
                      "item_code": "Envase de 5GL Iridium Blue",
                      "s_warehouse": SUCIOS,
                      "t_warehouse": location,
                      "serial_no": ", ".join(bottles)
                    }
                  ]
                }

                print("----- {}".format(body))

                stock_entry = frappe.get_doc(body)

                stock_entry.save()
                stock_entry.submit()

                LG("Commit: {}".format(location))
                frappe.db.commit()

            sleep(3)



    # print("CLXX0 : {}".format(purchase_orders['CLXX0']))
    # print("ALERTAR : {}".format(customers['ALERTAR']))
    # print("Envases Rotos : {}".format(customers['Envases Rotos']))
    # print("Envases Perdidos : {}".format(customers['Envases Perdidos']))

    LG("Ran quick test.")
    # LG(data['iTotalDisplayRecords'])

    return "Test Complete {}".format(str(int('5')).zfill(3))


# @frappe.whitelist()
# def installReturnables(company):
#     return install_returnables(company)


# @frappe.whitelist()
# def queueInstallReturnables(company):
#     frappe.enqueue(
#         'returnable.returnable.doctype.returnable.returnable.install_returnables',
#         company=company, is_async=True, timeout=240000)
#     return "Enqueued"
