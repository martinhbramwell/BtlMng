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
          "allow_zero_valuation_rate": 0,
          "s_warehouse": spec.src,
          "t_warehouse": spec.tgt
        },  {
          "qty": spec.qty,
          "item_code": "FICHA - para envase IB de 5GL",
          "s_warehouse": spec.src,
          "t_warehouse": spec.tgt,
          "allow_zero_valuation_rate": 1,
          "serial_no": spec.serial_no
        }]
    }

    print("----- {}".format(body))

    stock_entry = frappe.get_doc(body)

    stock_entry.save()
    stock_entry.submit()

    LG("        Commit: {} ==> {}".format(spec.sn_block, spec.tgt))
    frappe.db.commit()

    return stock_entry

def makeWarehouse(name, parent_warehouse='Envases IB Custodia del Cliente', account='1.1.5.06 - Envases Custodiados'):
    whs_name = "{} - {}".format(name, ABBR_COMPANY)
    parent_whs = "{} - {}".format(parent_warehouse, ABBR_COMPANY)
    acct = "{} - {}".format(account, ABBR_COMPANY)
    LG("Check if the warehouse '{}' exists".format(whs_name))
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
    envars = Path("{}/../apps/electronic_invoice/install_scripts/envars.sh".format(os.getcwd())).resolve()
    with open(envars, 'r') as input:
       for line in input:
           if 'COOKIE_VAL' in line:
                parts = re.search('COOKIE_VAL="(.+?)";', line)
                if parts:
                    cookie = parts.group(1)
                break

    return cookie

BOTTLE_LIST_FILE = "bottleList.json"
BOTTLE_LIST = LOG_DIR + "/" + BOTTLE_LIST_FILE
def getBottlesStatusFromBAPU(cookie):
    bottleList = ""
    if Path(BOTTLE_LIST).is_file():
        LG(f"==== Loading Bottles Status from {BOTTLE_LIST} ====")
        with open(BOTTLE_LIST) as f:
           bottleList = json.load(f)

    else:
        # LG("==== Obtaining Bottles Status from BAPU  (PHPSESSID: {}) ====".format(cookie))
        LG("==== Obtaining Bottles Status from BAPU ====")
        response = requests.get(BAPU_EP, headers={"Cookie": "PHPSESSID={}".format(cookie)})
        time.sleep(2)
        # LG("Response {}".format(response))
        respJSON = response.json()
        # LG("Response JSON {}".format(respJSON))
        bottleList = respJSON['aaData']
        # LG("Bottle List {}".format(len(bottleList)))
        with open(BOTTLE_LIST, 'w') as f:
            json.dump(bottleList, f)


    return bottleList

def prepareReferenceTables(bottlesStatusPage):
    fixLookUp = getBadDataLookupDict()

    customers = frappe._dict()
    bottle_blocks = frappe._dict()
    for bottle in bottlesStatusPage:
        # LG(f"Bottle :: {bottle}")
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
        }, {
            "item_code": "FICHA - para envase IB de 5GL",
            "qty": spec.quantity,
            "rate": 0,
            "warehouse": "Envases IB Sucios - LSSA"
        }]
    })

    purchase_order.save()
    purchase_order.submit()

    LG("Commit block:{}".format(spec.order_confirmation_no))
    frappe.db.commit()

    return purchase_order

def createPurchaseReceipt(spec):

    itemModel = frappe._dict({
        'docstatus': 0,
        'item_code': None,
        'qty': spec.quantity,
        "rate": 0,
        'received_stock_qty': spec.quantity,
        'warehouse': 'Envases IB Sucios - LSSA',
        'purchase_order': spec.purchase_order,
        'purchase_order_item': None,
        'allow_zero_valuation_rate': 0,
        'schedule_date': spec.schedule_date,
        'serial_no': None,
        'include_exploded_items': 0,
        'expense_account': '5.1.1.03 - Costos Sobre Ventas - LSSA'
    })

    items = []
    for po_item in spec.purchase_order_items:
        item = itemModel.copy()
        item.item_code = po_item.item_code
        item.purchase_order_item = po_item.name
        if 'FICHA' in po_item.item_code:
            item.serial_no = spec.serial_no
            item.allow_zero_valuation_rate = 1
        else:
            item['rate'] = 8.04
            item.serial_no = None

        # print(item)
        items.append(item)

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
        'items': items
    }

    # print(body)

    purchase_receipt = frappe.get_doc(body)

    # # LG("-----")

    purchase_receipt.save()
    purchase_receipt.submit()

    LG("      Commit receipt of PO: {}".format(spec.purchase_order))
    frappe.db.commit()

    return purchase_receipt

def getExistingPurchaseOrders():
    PO_tuple = frappe.db.get_list('Purchase Order',
        fields=['order_confirmation_no'],
        as_list=True
    )

    return [x for x, in PO_tuple]

def generatePurchaseOrders(bottle_blocks):
    LG("==== Generating Purchase Orders ====")

    POs = getExistingPurchaseOrders()
    LG(f"POs :: {POs}")

    purchase_orders = frappe._dict()
    idx = 0
    for block_id in bottle_blocks.keys():
        if block_id in POs :
            LG(f"   Purchase order for #{block_id} has already been created.")
            purchase_orders[block_id] = {}
        else:

            idx += 1
            item_count = len(bottle_blocks[block_id])

            LG(f"      {block_id} has {item_count} entries.")

            creation = pseudoDate("2015-12-{} 15:52", idx, True, True)
            xaction = pseudoDate("2015-12-{} 15:52", idx, True, False)
            scheduled = pseudoDate("2016-01-{} 15:52", idx, True, False)
            LG("      {} has {} entries. Created: {} Transaction: {} Scheduled: {}".format(block_id, item_count, creation, xaction, scheduled))

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

    LG("==== Generated Purchase Orders ====")
    return purchase_orders

def getExistingPurchaseReceiptPOs():
    POs = frappe.db.sql(
        """SELECT distinct purchase_order FROM `tabPurchase Receipt Item`""",
        as_list=True
    )
    # LG(f"POs :: {POs}")

    purchase_orders = []
    for PO in POs:
        # LG(f"PO :: {PO[0]}")
        purchase_orders.append(PO[0])

    # fields=['purchase_order'],    SELECT distinct purchase_order FROM `tabPurchase Receipt Item`;
    return purchase_orders

def generatePurchaseReceipts(serial_number_blocks):
    LG("\n==== Generating Purchase Receipts ====")

    PRPOs = getExistingPurchaseReceiptPOs()
    # LG(f"PRPOs :: {PRPOs}")

    all_purchase_orders = frappe.db.get_list('Purchase Order')

    purchase_receipts = frappe._dict()
    for po in all_purchase_orders:
        # LG(f"PO :: {po.name}")
        if po.name in PRPOs:
            LG(f"   Purchase receipt for PO #{po.name} has already been created.")
        else:
            purchase_receipt = frappe._dict()
            PurchaseOrder = frappe.get_doc('Purchase Order', po.name)
            po_seq = int(PurchaseOrder.name[13:18])

            creation = pseudoDate("2016-01-{} 15:52", po_seq, True, True)
            posting_date = pseudoDate("2016-01-{} 16:59", po_seq, True, False)
            posting_time = pseudoDate("2016-01-{} 16:59", po_seq, False, True)
            supplier = "Fabrica De Envases S. A. FADESA"

            purchase_order = PurchaseOrder.name
            # purchase_order_item = PurchaseOrder.items[0].name
            scheduled = pseudoDate("2016-01-{} 16:59", po_seq, True, False)

            block_id = PurchaseOrder.order_confirmation_no
            quantity = serial_number_blocks[block_id].qty
            serial_no = serial_number_blocks[block_id].sns

            LG("      PO #{}: {} matched with {} having {} bottles".format(str(po_seq).zfill(2), purchase_order, block_id, quantity))
            # print( "Creation: {}. Posting Date: {},  Time: {}.  Scheduled: {}".format(creation, posting_date, posting_time, scheduled))

            purchase_receipt['pr'] = createPurchaseReceipt(frappe._dict({
                'creation': creation,
                'posting_date': posting_date,
                'posting_time': posting_time,
                'supplier': supplier,
                'purchase_order': purchase_order,
                'purchase_order_items': PurchaseOrder.items,
                'schedule_date': scheduled,
                'quantity': quantity,
                'serial_no': serial_no
            }))

            purchase_receipts.setdefault(block_id, purchase_receipt)
    LG("==== Generated Purchase Receipts ====\n")
    return

def transferBottles(target, serial_number_blocks):
    LG("==== Transfer Bottles Block to {} ====".format(target))
    for block_id in serial_number_blocks:
        bottle_block = serial_number_blocks[block_id][target]
        bottles = bottle_block.sns
        qty = bottle_block.qty
        if qty > 0:
            LG("        Transferring {} ({}) to {}".format(block_id, qty, target))
            LG("{}".format(bottles))

            spec = frappe._dict({
                'sn_block': block_id,
                'qty': qty,
                'src': SUCIOS,
                'tgt': target,
                'serial_no': bottles
            })

            createStockEntry(spec)

        sleep(1)
    LG("      Transferred")

def relocateBottlesInternally(serial_number_blocks):
    LG("==== Relocating Bottles Internally ====")
    locations = [ROTOS, PERDIDOS, ALERTAR, LLENOS]
    for location in locations:
        transferBottles(location, serial_number_blocks)
    LG("==== Relocated Bottles Internally ====")

def instantiateWarehouseForEachCustomer(customers):
    for customer_name in sorted(customers.keys()):
        if customer_name not in [ "ALERTAR", "Envases Rotos", "Envases Perdidos"]:
            location = makeWarehouse(customer_name.strip())
            print("New/existing stock location: >{}<".format(location))

def getSerialNumbers(bottle_blocks):
    LG("==== Collecting Serial Numbers ====")
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

        serial_numbers["sns"] = "\n".join(serial_no)
        serial_numbers["qty"] = len(serial_no)

        serial_numbers[PERDIDOS] = frappe._dict({ "sns": "\n".join(perdidos), "qty": len(perdidos)})
        serial_numbers[ALERTAR] = frappe._dict({ "sns": "\n".join(alertar), "qty": len(alertar)})
        serial_numbers[ROTOS] = frappe._dict({ "sns": "\n".join(rotos), "qty": len(rotos)})
        serial_numbers[SUCIOS] = frappe._dict({ "sns": "\n".join(sucios), "qty": len(sucios)})
        serial_numbers[LLENOS] = frappe._dict({ "sns": "\n".join(llenos), "qty": len(llenos)})

        serial_numbers["cliente"] = frappe._dict({ "sns": "\n".join(cliente), "qty": len(cliente)})

        # serial_numbers[ALERTAR] = "\n".join(alertar)
        # serial_numbers[ROTOS] = "\n".join(rotos)
        # serial_numbers[SUCIOS] = "\n".join(sucios)
        # serial_numbers[LLENOS] = "\n".join(llenos)

        # serial_numbers["cliente"] = "\n".join(cliente)


        serial_number_blocks[block_id] = serial_numbers
        LG("      Block {}: Perdidos {}, Alertar: {}, Rotos: {}, Sucios: {}, Llenos: {}".format(
            block_id, len(perdidos), len(alertar), len(rotos), len(sucios), len(llenos)
        ))

    return serial_number_blocks

def moveBottlesToCustomers(customers):
    LG("\n\nPause to allow prior transactions to complete...")
    sleep(30)
    LG("==== Relocating Bottles To Customer Consignment ====")
    for customer_name in sorted(customers.keys()):
        if customer_name not in [ "ALERTAR", "Envases Rotos", "Envases Perdidos", "0" ]:
            item_count = len(customers[customer_name])
            customer = frappe.get_doc('Customer', customer_name)
            # LG("{} ({}) has {} entries.".format(customer_name, customer.gender, item_count))
            bottles = []
            for bottle_block in customers[customer_name]:
                bottles.append(bottle_block[1])
                # LG("    Bottles {}.".format(bottles))
                # print("    Bottles {}.".format(bottle_block))

            qty = len(bottles)
            if qty > 0:
                location = "{} - {}".format(customer_name.strip(), ABBR_COMPANY)
                body = {
                  "doctype": "Stock Entry",
                  "docstatus": 0,
                  "naming_series": "MAT-STE-.YYYY.-",
                  "stock_entry_type": "Material Transfer",
                  "title": "Move {} bottles to {}".format(qty, location),
                  "items": [
                    {
                      "qty": qty,
                      "item_code": "Envase de 5GL Iridium Blue",
                      "s_warehouse": SUCIOS,
                      "allow_zero_valuation_rate": 0,
                      "t_warehouse": location
                    }, {
                      "qty": qty,
                      "item_code": "FICHA - para envase IB de 5GL",
                      "s_warehouse": SUCIOS,
                      "allow_zero_valuation_rate": 1,
                      "serial_no": ", ".join(bottles),
                      "t_warehouse": location
                    }]
                }

                LG("----- {}".format(body))

                stock_entry = frappe.get_doc(body)

                stock_entry.save()
                stock_entry.submit()

                LG("Committing a {} bottle Stock Entry for {}".format(qty, location))
                frappe.db.commit()

            sleep(1)
    LG("==== Relocated Bottles To Customer Consignment ====")

@frappe.whitelist()
def tester(company):
    LG("Getting values for company :: {}".format(company))
    prepareGlobals(company)
    print("Starting Test")

    idx = 15
    creation = pseudoDate("2015-12-{} 15:52", idx, True, True)
    xaction = pseudoDate("2015-12-{} 15:52", idx, True, False)
    scheduled = pseudoDate("2016-01-{} 15:52", idx, True, False)


    if ( 0 == 1 ):
        po = createPurchaseOrder(frappe._dict({
            'supplier': "Fabrica De Envases S. A. FADESA",
            'order_confirmation_no': "IBXX5",
            'creation': creation,
            'transaction_date': xaction,
            'schedule_date': scheduled,
            'quantity': 10
        }))
    else:
        po = frappe._dict({ "name": "PUR-ORD-2021-00022" })

    purchase_order = frappe.get_doc("Purchase Order", po.name)

    print("PO: {} Line Item: {}".format(purchase_order.name, purchase_order.items[0].name))


    if ( 0 == 1 ):
        purchase_order_name = purchase_order.name
        purchase_order_item = purchase_order.items[0].name
        quantity = purchase_order.items[0].qty

        dt = 15
        creation = pseudoDate("2016-02-{} 16:59", dt, True, True)
        posting_date = pseudoDate("2016-02-{} 16:59", dt, True, False)
        posting_time = pseudoDate("2016-02-{} 16:59", dt, False, True)
        schedule_date = pseudoDate("2016-02-{} 16:59", dt, True, False)

        serial_no = "IBXX550\nIBXX551\nIBXX552\nIBXX553\nIBXX554\nIBXX555\nIBXX556\nIBXX557\nIBXX558\nIBXX559"

        pr_spec = {
            'creation': creation,
            'posting_date': posting_date,
            'posting_time': posting_time,
            'supplier': "Fabrica De Envases S. A. FADESA",
            'purchase_order': purchase_order_name,
            'purchase_order_item': purchase_order_item,
            'schedule_date': scheduled,
            'quantity': quantity,
            'serial_no': serial_no
        }
        print("PR: {}".format(pr_spec))

        # pr = frappe._dict({ "name": "MAT-PRE-2021-00012" })
        pr = createPurchaseReceipt(frappe._dict(pr_spec))

        # print("PR: {}".format(pr))
    else:
        pr = frappe._dict({ "name": "MAT-PRE-2021-00016" })

    purchase_receipt = frappe.get_doc("Purchase Receipt", pr.name)
    # serial_numbers = purchase_receipt.items[0].serial_no
    serial_numbers = [ "IBXX554", "IBXX555" ]
    print("PR: {}".format(purchase_receipt.name))
    print("Serial Numbers: \n{}".format(serial_numbers))

    if ( 0 == 1 ):
        # qty = purchase_receipt.items[0].qty
        qty = 2
        target = ROTOS
        se_spec = frappe._dict({
            'sn_block': SUCIOS,
            'qty': qty,
            'src': SUCIOS,
            'tgt': target,
            'serial_no': ", ".join(serial_numbers)
        })
        print("SE: {}".format(se_spec))

        # se = frappe._dict({ "name": "MAT-STE-2021-00476" })
        se = createStockEntry(se_spec)

    else:
        se = frappe._dict({ "name": "MAT-STE-2021-00478" })

    stock_entry = frappe.get_doc("Stock Entry", se.name)
    print("SE: {}".format(stock_entry.name))
    print("Serial Numbers: \n{}".format(stock_entry.items[0].serial_no))

    if ( 1 == 1 ):
        # qty = purchase_receipt.items[0].qty
        qty = 2
        target = ALERTAR
        se_spec = frappe._dict({
            'sn_block': ROTOS,
            'qty': qty,
            'src': ROTOS,
            'tgt': target,
            'serial_no': ", ".join(serial_numbers)
        })
        print("SE: {}".format(se_spec))

        # se = frappe._dict({ "name": "MAT-STE-2021-00476" })
        se = createStockEntry(se_spec)

    else:
        se = frappe._dict({ "name": "MAT-STE-2021-00478" })

    stock_entry = frappe.get_doc("Stock Entry", se.name)
    print("SE: {}".format(stock_entry.name))
    print("Serial Numbers: \n{}".format(stock_entry.items[0].serial_no))


    print("Finished Test")

@frappe.whitelist()
def process(company):
    LG("Getting values for company :: {}".format(company))
    prepareGlobals(company)

    # print(" Envars:: {} ".format(Path("{}/../apps/electronic_invoice/install_scripts/envars.sh".format(os.getcwd())).resolve()))
    # print(getBAPUCookie())

    bottlesStatusPage = getBottlesStatusFromBAPU(getBAPUCookie())
    LG("    Bottles status page has {} bottles".format(len(bottlesStatusPage)))
    # # print(f"Bottles status page :: {bottlesStatusPage}")

    customers, bottle_blocks = prepareReferenceTables(bottlesStatusPage)
    # print(f"customers: {json.dumps(customers, indent=4)}")
    # print(f"bottle_blocks: {json.dumps(bottle_blocks, indent=4)}")

    serial_number_blocks = getSerialNumbers(bottle_blocks)
    # print(f"serial_number_blocks: {json.dumps(serial_number_blocks, indent=4)}")

    instantiateWarehouseForEachCustomer(customers)

    purchase_orders = generatePurchaseOrders(bottle_blocks)
    # LG(f"Purchase Orders :: {purchase_orders}")

    generatePurchaseReceipts(serial_number_blocks)

    relocateBottlesInternally(serial_number_blocks)

    moveBottlesToCustomers(customers)

    LG("Stock Initialization Complete.")

    # return "Stock Initialization Complete".format()

@frappe.whitelist()
def initializeStock(company):
    return process(company)

@frappe.whitelist()
def queueInitializeStock(company):
    frappe.enqueue(
        'returnable.returnable.doctype.returnable.initialize_stock.process',
        company=company, is_async=True, timeout=240000)
    return "Enqueued"

@frappe.whitelist()
def se_count(company):
    prepareGlobals(company)

    data = frappe.db.sql("""SELECT count(*) FROM `tabStock Entry` se""", as_dict=0)
    cnt = data[0][0]
    # LG("-- {}".format(cnt), logname = "{}/notification.log".format(LOG_DIR))

    LG("{}".format(cnt), logname="{}/notification.log".format(LOG_DIR))
    LG("-- {}  | ".format(cnt))

    return "{} Stock Entries".format(cnt)
