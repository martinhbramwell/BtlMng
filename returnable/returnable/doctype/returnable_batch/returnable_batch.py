# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document

TOCUST = '> Cust'
TOSTOCK = '> Stock'
FROMCUST = 'Cust >'
FROMSTOCK = 'Stock >'

CUSTCUST = FROMCUST + TOCUST
CUSTSTOCK = FROMCUST + TOSTOCK
STOCKCUST = FROMSTOCK + TOCUST
STOCKSTOCK = FROMSTOCK + TOSTOCK

qryGetState = "SELECT code FROM `tabReturnable` where state = '{0}' and code in ({1})";

FULL = 'Lleno'
INDETERMINATE = 'Confuso'
DIRTY = 'Sucio'
AT_CUSTOMER = 'Donde Cliente'

stateLookup = {
  'Envases IB Llenos - LSSA': FULL,
  'Envases IB Rotos - LSSA': INDETERMINATE,
  'Envases IB Sucios - LSSA': DIRTY
}

# lst = [['a', ''], ['b', ''], ['c', ''], ['d', '']]
# csvString
def list2String(lst):
  sep = ''
  csvString = ''
  for val in lst:
    csvString += sep + '"' + val + '"'
    sep = ','
  return csvString

def listReturnablesMoved(moved):
  rets = []
  for returnable in moved:
      rets.append(returnable.bottle)
  return rets

def custCust(frm):
  print('custCust :: ' + frm.direction)
  tc = frm.to_customer;
  fc = frm.from_customer;

  if tc == fc:
    exceptionMessages.append('No hay como mover envases entre "{0}" y "{1}" '.format(tc, fc))

  if not fc:
    exceptionMessages.append('Debe especificar el cliente de origen.')

  if not tc:
    exceptionMessages.append('Debe especificar el cliente destinatario.')

  toBeMoved = listReturnablesMoved(frm.bottles_moved)
  # query = qryGetState.format(AT_CUSTOMER, list2String(toBeMoved))
  # print(qryGetState.format(AT_CUSTOMER, list2String(toBeMoved)))

  actualReturnablesAtCustomer = frappe.db.sql(qryGetState.format(AT_CUSTOMER, list2String(toBeMoved)))
  lstUnavailables = [x for x in toBeMoved if x not in [r[0] for r in actualReturnablesAtCustomer]]
  ul = len(lstUnavailables)
  if 0 < len(lstUnavailables):
    exceptionMessages.append(
      noSuchProduct.format(fc, 'el' if ul == 1 else 'los', '' if ul == 1 else 's', list2String(lstUnavailables))
    )
  # raise Exception('No validation for: {}'.format(CUSTCUST))

def custStock(frm):
  print('custStock :: ' + frm.direction)
  fc = frm.from_customer;
  ts = frm.to_stock;

  toBeMoved = listReturnablesMoved(frm.bottles_moved)
  actualReturnablesAtCustomer = frappe.db.sql(qryGetState.format(AT_CUSTOMER, list2String(toBeMoved)))
  lstUnavailables = [x for x in toBeMoved if x not in [r[0] for r in actualReturnablesAtCustomer]]

  ul = len(lstUnavailables)

  if 0 < len(lstUnavailables):
    exceptionMessages.append(
      noSuchProduct.format(fs, 'el' if ul == 1 else 'los', '' if ul == 1 else 's', list2String(lstUnavailables))
    )

  if not fc:
    exceptionMessages.append('Debe especificar el cliente de origen.')

  if not ts:
    exceptionMessages.append('Debe especificar el almacen destinatario.')

def stockCust(frm):
  fs = frm.from_stock;
  tc = frm.to_customer;
  # print('stockCust :: ' + frm.direction)
  # print(frm.from_stock)

  toBeMoved = listReturnablesMoved(frm.bottles_moved)
  # print(list2String(toBeMoved))

  # query = qryGetState.format(FULL, list2String(toBeMoved))
  # print(qryGetState.format(FULL, list2String(toBeMoved)))

  actualReturnablesInWarehouse = frappe.db.sql(qryGetState.format(FULL, list2String(toBeMoved)))
  # print("actualReturnablesInWarehouse {0} ".format(actualReturnablesInWarehouse))
  # print(type(actualReturnablesInWarehouse))
  # lstReturnables = [r[0] for r in actualReturnablesInWarehouse]
  lstUnavailables = [x for x in toBeMoved if x not in [r[0] for r in actualReturnablesInWarehouse]]
  # print(type([r[0] for r in actualReturnablesInWarehouse]))
  # print(len(lstReturnables))
  # print(type(lstUnavailables))
  # print(len(lstUnavailables))

  ul = len(lstUnavailables)

  if 0 < len(lstUnavailables):
    exceptionMessages.append(
      noSuchProduct.format(fs, 'el' if ul == 1 else 'los', '' if ul == 1 else 's', list2String(lstUnavailables))
    )

  if not fs:
    exceptionMessages.append('Debe especificar el almacen de origen.')

  if not tc:
    exceptionMessages.append('Debe especificar el cliente destinatario.')


  # raise Exception('No validation for: {}'.format(STOCKCUST))

def stockStock(frm):
  print('stockStock :: ' + frm.direction)
  fs = frm.from_stock;
  ts = frm.to_stock;
  state = stateLookup.get(fs, AT_CUSTOMER)
  if state == AT_CUSTOMER:
    exceptionMessages.append('No se puede mover envases desde "{0}" '.format(fs))

  ts = frm.to_stock;
  if stateLookup.get(ts, AT_CUSTOMER) == AT_CUSTOMER:
    exceptionMessages.append('No se puede mover envases a "{0}" '.format(ts))

  if ts == fs:
    exceptionMessages.append('No hay como mover envases entre "{0}" y "{1}" '.format(ts, fs))

  if not fs:
    exceptionMessages.append('Debe especificar el almacen de origen.')

  if not ts:
    exceptionMessages.append('Debe especificar el almacen destinatario.')


  toBeMoved = listReturnablesMoved(frm.bottles_moved)
  actualReturnablesInWarehouse = frappe.db.sql(qryGetState.format(state, list2String(toBeMoved)))
  lstUnavailables = [x for x in toBeMoved if x not in [r[0] for r in actualReturnablesInWarehouse]]
  ul = len(lstUnavailables)
  if 0 < len(lstUnavailables):
    exceptionMessages.append(
      noSuchProduct.format(fs, 'el' if ul == 1 else 'los', '' if ul == 1 else 's', list2String(lstUnavailables))
    )


directions = {}
directions[CUSTCUST] = custCust
directions[CUSTSTOCK] = custStock
directions[STOCKCUST] = stockCust
directions[STOCKSTOCK] = stockStock

exceptionMessages = ['Errores:']
# exceptionMessages = ['']
noSuchProduct = 'Almacen "{0}" no tiene {1} producto{2} : {3}'

class ReturnableBatch(Document):
	
  def validate(self):

    exceptionMessages.append('DUMMY')

    print(' *** *** *** ***  Direction ', self.direction, ' <> ', ' *** *** *** *** *** ');
    directions[self.direction](self)


    if 1 < len(exceptionMessages):
      exceptionMessage = ''
      sep = ''
      bullet = 1
      for msg in exceptionMessages: 
        exceptionMessage += sep + msg
        sep = '\n ' + str(bullet) + ') '
        bullet += 1
      print(exceptionMessage)
      exceptionMessages.clear()
      exceptionMessages.append('Errores:')
      frappe.throw(_(exceptionMessage))

# @frappe.whitelist()
# def loadReturnablesStates(direction):
#   # msgprint(_("Direction is :: {0} ").format(direction) )
#   actualReturnablesInWarehouse = frappe.db.sql("select count(*) from `tabReturnable`");

#   print(' *** *** *** ***  Direction ', direction, ' <> ', type(actualReturnablesInWarehouse), ' *** *** *** *** *** ');
#   return ("Returnables Count :: {0} ").format(actualReturnablesInWarehouse);
