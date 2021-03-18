# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

import os
import time

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

  EXISTING_LOCATIONS = set({ SUCIOS, LLENOS, ROTOS })


def LG(txt, end = "\n", logname = "{}/result.log".format(LOG_DIR)):
  # logname = "/dev/shm/erpnext/result.log"
  if os.path.exists(logname):
    append_write = 'a' # append if already exists
  else:
    try:
      if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    except OSError as e:
      if e.errno != errno.EEXIST:
            raise
    append_write = 'w' # make a new file if not

  logfile = open(logname,append_write)
  logfile.write(txt + end)
  logfile.close()




class Returnable(Document):
  pass

def getQryReturnable(returnable = '%', state = '%', offset = 0, rows = 0):
  limit = "" if offset + rows == 0 else "LIMIT {}, {}".format(offset, rows)
  return """
      SELECT *
        FROM `tabReturnable` R
       WHERE name LIKE '{0}'
         AND state LIKE '{1}'
         AND last_customer not like 'Abner Victor%'
    ORDER BY last_customer
       {2}
       ;
  """.format(returnable, state, limit)


def processSimple(list, name):
  LG("\n")
  numbers = []
  for returnable in list:
    LG("{} : '{}'".format(name, returnable.name))
    numbers.append(returnable.name)

  LG("Create Stock Entry for : {}".format(numbers))
  createStockEntry(frappe._dict({ 'serial_numbers': numbers, 'warehouse_name': name}))

def processFull(list):
  processSimple(list, LLENOS)

def processDirty(list):
  processSimple(list, SUCIOS)


def processReturnable(returnable):
  LG("Returnable ==> {}.  State {}.  Last cust {}.".format(returnable.name, returnable.state, returnable.last_customer))

def createStockEntry(spec):
  # LG("Create {} item stock entry to {}.".format(len(spec.serial_numbers), spec.warehouse_name))

  stock_entry = frappe.get_doc({
    'doctype': 'Stock Entry',
    'docstatus': 0,
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


def createStockEntryForCustomer(returnable, numbers):
  # LG("Create {} item stock entry for customer :: {}.  ({})".format(len(numbers), returnable.last_customer, NAME_COMPANY))
  
  whs_name = "{} - {}".format(returnable.last_customer, ABBR_COMPANY)
  ccw = frappe.get_doc('Warehouse', whs_name)

  LG("Creating '{}' item Stock Entry for {}".format(numbers, ccw.name))
  createStockEntry(frappe._dict({
    'serial_numbers': numbers,
    'warehouse_name': ccw.name
  }))


def processByCustomer(list):

  LG("\n")
  # LG("By customer : {}".format(len(list)))
  customer = ''
  numbers = []
  previousReturnable = {}

  for returnable in list:
    if customer == returnable.last_customer or customer == '':
      numbers.append(returnable.name)
    else:
      createStockEntryForCustomer(previousReturnable, numbers)
      numbers.clear()
      numbers.append(returnable.name)

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
      ccw = frappe.get_doc('Warehouse', whs_name)
      # LG("Warehouse '{}' already exists".format(ccw.name))
    except:
      LG("Creating warehouse '{}'.".format(whs_name))
      customer_consignment_warehouse = frappe.get_doc({
        'doctype': 'Warehouse',
        'warehouse_name': returnable.last_customer,
        'parent_warehouse': "{} - {}".format('Envases IB Custodia del Cliente', ABBR_COMPANY),
        'company': NAME_COMPANY,
        'account': "{} - {}".format('1.1.5.06 - Envases Custodiados', ABBR_COMPANY),
        'warehouse_type': 'Consignado'
      })

      customer_consignment_warehouse.save()
      customer_consignment_warehouse.submit()
      LG("- o 0 o -")



def processReturnables(query, func):
  returnables = frappe.db.sql(query, as_dict=True)
  func(returnables)
  return len(returnables)

def processReturnablesGroup(group, func):
  rows = cnt = 50
  offset = 0
  sleep = 2 # seconds
  while cnt == rows:
    query = getQryReturnable(returnable = 'IB%', state = group, rows = rows, offset = offset)
    cnt = processReturnables(query, func)
    offset = offset + rows
    # LG("count {}, sleep {}".format(cnt, sleep))
    # time.sleep(2)

def install_returnables(company):
  LG("Getting values for company :: {}".format(company))
  prepareGlobals(company)

  LG("\n\nCreate {} customer consignment warehouses.".format(NAME_COMPANY))
  processReturnablesGroup('Donde Cliente', makeWarehouses)

  LG("\n\nProcess Customer Returnables")
  processReturnablesGroup('Donde Cliente', processByCustomer)

  LG("\n\nProcess Full Returnables")
  processReturnablesGroup('Lleno', processFull)

  LG("\n\nProcess Dirty Returnables ")
  processReturnablesGroup('Sucio', processDirty)

  LG("Completed all blocks")

  return "Installed Returnables";

@frappe.whitelist()
def se_count(company):
  LG("+++++++++++++")
  prepareGlobals(company)

  data = frappe.db.sql("""SELECT count(*) FROM `tabStock Entry` se""", as_dict=0)
  cnt = data[0][0]
  # LG("-- {}".format(cnt), logname = "{}/notification.log".format(LOG_DIR))
  
  LG("{}".format(cnt), logname = "{}/notification.log".format(LOG_DIR))
  LG("-- {}  | ".format(cnt))

  return "{} Stock Entries".format(cnt);

@frappe.whitelist()
def tester(company):
  LG("Getting values for company :: {}".format(company))
  prepareGlobals(company)

  data = frappe.db.sql("""SELECT count(*) FROM `tabStock Entry` se""", as_dict=0)
  LG("{}".format(data))

  return "Test Complete"

@frappe.whitelist()
def installReturnables(company):
  return install_returnables(company)

@frappe.whitelist()
def queueInstallReturnables(company):
  frappe.enqueue('returnable.returnable.doctype.returnable.returnable.install_returnables',
    company=company,
    is_async=True,
    timeout=240000
  )
  return "Enqueued"
