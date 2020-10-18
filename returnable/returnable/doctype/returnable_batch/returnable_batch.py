# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import inspect
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document

qryGetState = """
    SELECT code
      FROM `tabReturnable`
     WHERE state = '{0}'
       AND code IN ({1})
""";

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
  try:
    for val in lst:
      csvString += sep + '"' + val + '"'
      sep = ','
  except:
    pass

  return csvString

def getReturnablesList(moved):
  rets = []
  try:
    for returnable in moved:
      rets.append(returnable.bottle)
  except:
    pass

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

  toBeMovedNow = getReturnablesList(frm.bottles_moved)
  # qryLocationsOfMovedItems = qryGetState.format(AT_CUSTOMER, list2String(toBeMovedNow))
  # print(qryGetState.format(AT_CUSTOMER, list2String(toBeMovedNow)))

  actualReturnablesAtCustomer = frappe.db.sql(qryGetState.format(AT_CUSTOMER, list2String(toBeMovedNow)))
  lstUnavailables = [x for x in toBeMovedNow if x not in [r[0] for r in actualReturnablesAtCustomer]]
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

  toBeMovedNow = getReturnablesList(frm.bottles_moved)
  print(qryGetState.format(FULL, list2String(toBeMovedNow)))
  actualReturnablesAtCustomer = frappe.db.sql(qryGetState.format(AT_CUSTOMER, list2String(toBeMovedNow)))
  lstUnavailables = [x for x in toBeMovedNow if x not in [r[0] for r in actualReturnablesAtCustomer]]

  ul = len(lstUnavailables)

  if 0 < len(lstUnavailables):
    exceptionMessages.append(
      noSuchProduct.format(fc, 'el' if ul == 1 else 'los', '' if ul == 1 else 's', list2String(lstUnavailables))
    )

  if not fc:
    exceptionMessages.append('Debe especificar el cliente de origen.')

  if not ts:
    exceptionMessages.append('Debe especificar el almacen destinatario.')

# saved = 0
# submitted = 1
tmpltQryLocationsOfMovedItems = """
    SELECT
          B.direction     as `Direccion`
        , B.to_customer   as `Al Cliente`
        , B.to_stock      as `Al Almacén`
        , B.from_customer as `Del Cliente`
        , B.from_stock    as `Del Almacén`
        , C.Retornable    as `Retornable`
        , B.name          as `Lote`
        , I.name          as `Item`
        , B.timestamp     as `Fecha`
        , B.docstatus     as `Estado`
        , B.bapu_id       as `ID_BAPU`
      FROM
          `tabReturnable Batch` B
INNER JOIN (
        SELECT Retornable, MAX(Fecha) as Fecha
          FROM (
               SELECT
                     MAX(M.timestamp) as Fecha
                   , N.bottle as Retornable
                   , M.direction as Direccion
                 FROM
                     `tabReturnable Batch` M
                   , `tabReturnable Batch Item` N
                WHERE N.parent = M.name
                  AND N.bottle in ({0})
                  AND M.docstatus = 1
             GROUP BY Retornable, Direccion
          ) A
        GROUP BY Retornable
      ) C ON C.Fecha = B.timestamp
         , `tabReturnable Batch Item` I
      WHERE
           I.parent = B.name
       AND C.Retornable = I.bottle
       AND B.docstatus = 1
       AND I.bottle in ({0})
""";

TOCUST = '> Cust'
TOSTOCK = '> Stock'
FROMCUST = 'Cust >'
FROMSTOCK = 'Stock >'

CUSTCUST = FROMCUST + TOCUST
CUSTSTOCK = FROMCUST + TOSTOCK
STOCKCUST = FROMSTOCK + TOCUST
STOCKSTOCK = FROMSTOCK + TOSTOCK

Src_Dest = {}
Src_Dest[CUSTCUST] = { "s": 3, "d": 1 }
Src_Dest[CUSTSTOCK] = { "s": 3, "d": 2 }
Src_Dest[STOCKCUST] = { "s": 4, "d": 1 }
Src_Dest[STOCKSTOCK] = { "s": 4, "d": 2 }

DirFlag = 0
Rtrnbl = 5


def validateStockCust(frm):
  fs = frm.from_stock;
  tc = frm.to_customer;
  print('*********   ' + inspect.currentframe().f_code.co_name + ' :: ' + frm.direction + '   *****')
  print(frm.from_stock)

  # toBeMovedNow = getReturnablesList(frm.bottles_moved)
  # print(list2String(toBeMovedNow))

  # qryLocationsOfMovedItems = tmpltQryLocationsOfMovedItems.format(list2String(toBeMovedNow))
  # print(tmpltQryLocationsOfMovedItems.format(list2String(toBeMovedNow)))

  # locationsOfMovedItems = frappe.db.sql(tmpltQryLocationsOfMovedItems.format(list2String(toBeMovedNow)))
  # print("locationsOfMovedItems {0} ".format(locationsOfMovedItems))
  # # print(type(locationsOfMovedItems))
  # # lstReturnables = [r[0] for r in locationsOfMovedItems]
  # lstUnavailables = [x for x in toBeMovedNow if x not in [r[0] for r in locationsOfMovedItems]]
  # # print(type([r[0] for r in locationsOfMovedItems]))
  # # print(len(lstReturnables))
  # # print(type(lstUnavailables))
  # # print(len(lstUnavailables))

  # ul = len(lstUnavailables)

  # if 0 < len(lstUnavailables):
  #   exceptionMessages.append(
  #     noSuchProduct.format(fs, 'el' if ul == 1 else 'los', '' if ul == 1 else 's', list2String(lstUnavailables))
  #   )

  # if not fs:
  #   exceptionMessages.append('Debe especificar el almacen de origen.')

  # if not tc:
  #   exceptionMessages.append('Debe especificar el cliente destinatario.')


def submitStockCust(frm):
  print('submitStockCust :: ' + frm.direction)

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


  toBeMovedNow = getReturnablesList(frm.bottles_moved)
  actualReturnablesInWarehouse = frappe.db.sql(qryGetState.format(state, list2String(toBeMovedNow)))
  lstUnavailables = [x for x in toBeMovedNow if x not in [r[0] for r in actualReturnablesInWarehouse]]
  ul = len(lstUnavailables)
  if 0 < len(lstUnavailables):
    exceptionMessages.append(
      noSuchProduct.format(fs, 'el' if ul == 1 else 'los', '' if ul == 1 else 's', list2String(lstUnavailables))
    )

# @frappe.whitelist()
# def loadReturnablesStates(direction):
#   # msgprint(_("Direction is :: {0} ").format(direction) )
#   actualReturnablesInWarehouse = frappe.db.sql("select count(*) from `tabReturnable`");

#   print(' *** *** *** ***  Direction ', direction, ' <> ', type(actualReturnablesInWarehouse), ' *** *** *** *** *** ');
#   return ("Returnables Count :: {0} ").format(actualReturnablesInWarehouse);


directions = {}
directions[CUSTCUST] = custCust
directions[CUSTSTOCK] = custStock
directions[STOCKCUST] = {}
directions[STOCKCUST]['validate'] = validateStockCust
directions[STOCKCUST]['on_submit'] = submitStockCust
directions[STOCKSTOCK] = stockStock

exceptionMessages = ['Errores:']
# exceptionMessages = ['']
noSuchProduct = 'Almacen "{0}" no tiene {1} producto{2} : {3}'


def getReturnablesToBeChecked(self):

    previouslyMoved = []
    try:
      previouslyMoved = getReturnablesList(self.get_doc_before_save().bottles_moved)
    except:
      pass

    print('Previously Moved :: {0}'.format(list2String(previouslyMoved)))

    toBeMovedNow = getReturnablesList(self.bottles_moved)
    print('To Be Moved Now  :: {0}'.format(list2String(toBeMovedNow)))

    unCheckedReturnables = list(set(toBeMovedNow) - set(previouslyMoved))
    print('Returnables To Be Checked :: {0}'.format(list2String(unCheckedReturnables)))

    return unCheckedReturnables


def validater(self):
    print('');
    print('');
    print('');
    print('');
    print('');
    print(' -----------------' + inspect.currentframe().f_code.co_name + '  ---------------------- ');

    # exceptionMessages.append('DUMMY')

    print('Direction : {0}'.format(self.direction))

    print('From Stock : {0}, From Customer : {1}'
      .format(self.from_stock, self.from_customer))
    print('To Stock : {0}, To Customer : {1}'
      .format(self.to_stock, self.to_customer))

    # intendedMoveTo = self.direction.split(' >> ')[1]
    intendedMoveFrom = self.direction.split(' >> ')[0]
    shouldBeAt = self.from_stock if intendedMoveFrom == 'Stock' else self.from_customer
    print("Expected source for move: '{0}' - '{1}'".format(intendedMoveFrom, shouldBeAt))

    returnablesToBeChecked = getReturnablesToBeChecked(self)

    numberOfReturnablesToBeChecked = len(returnablesToBeChecked)
    # print("Number Of Returnables To Be Checked {0} ".format(numberOfReturnablesToBeChecked))
    if numberOfReturnablesToBeChecked > 0:
      print("Returnables To Be Checked {0} ".format(returnablesToBeChecked[numberOfReturnablesToBeChecked - 1]))

      qryLocationsOfMovedItems = tmpltQryLocationsOfMovedItems.format(list2String(returnablesToBeChecked))
      # print(qryLocationsOfMovedItems)

      locationsOfMovedItems = frappe.db.sql(qryLocationsOfMovedItems)

      numberOfLocations = len(locationsOfMovedItems)
      print("Number of Locations Of MovedItems :: {0} ".format(numberOfLocations))
      if numberOfLocations > 0:
        N = numberOfLocations - 1
        L = locationsOfMovedItems[N - 1]
        D = L[DirFlag]
        R = L[Rtrnbl]
        S = L[Src_Dest[D]["s"]]
        A = L[Src_Dest[D]["d"]]
        print("Actual Moved Item #{0} :: Returnable - '{1}', Direction - '{2}', Source - '{3}', Last Location - '{4}' ".format(N, R, D, S, A))

        errMsgTmplt = """Se esperaba que el retornable '{0}' estuviera en '{3}' pero se movió por última vez a '{1} :: {2}'"""
        for location in locationsOfMovedItems:
          direction = location[DirFlag]
          returnable = location[Rtrnbl]
          oldMoveTarget = direction.split(' >> ')[1]
          oldMoveSource = location[Src_Dest[direction]["s"]]
          currentlyAt = location[Src_Dest[direction]["d"]]

          errMsg = errMsgTmplt.format(returnable, oldMoveTarget, currentlyAt, shouldBeAt)
          if ( currentlyAt != shouldBeAt ): exceptionMessages.append(errMsg)

      else:
        exceptionMessages.append('Ninguno de esos retornables fue encontrado')
      # # directions[self.direction][inspect.currentframe().f_code.co_name](self)

      # print('Preparing Exception Message ............')
      if 1 < len(exceptionMessages):
        exceptionMessage = ''
        sep = ''
        bullet = 1
        for msg in exceptionMessages: 
          exceptionMessage += sep + msg
          sep = '\n ' + str(bullet) + ') '
          bullet += 1
        exceptionMessages.clear()
        exceptionMessages.append('Errores:')
        frappe.throw(_(exceptionMessage))


class ReturnableBatch(Document):
  
  # def validate(self):
  #   print(' -----------------' + inspect.currentframe().f_code.co_name + '  ---------------------- ');

  def autoname(self):

    print(' -----------------' + inspect.currentframe().f_code.co_name + '  ---------------------- ');

  def before_insert(self):
    print(' -----------------' + inspect.currentframe().f_code.co_name + '  ---------------------- ');
    validater(self)

  def on_update(self):
    print(' -----------------' + inspect.currentframe().f_code.co_name + '  ---------------------- ');
    validater(self)
      # print('Saving not updating')

  def on_submit(self):
    print(' -----------------' + inspect.currentframe().f_code.co_name + '  ---------------------- ');
    print(self);

    # print(inspect.stack()[0][3]);    

    # print(' *** *** *** ***  Direction ', self.direction, ' <> ', ' *** *** *** *** *** ');
    # directions[self.direction][inspect.currentframe().f_code.co_name](self)

    # frappe.throw(_('  fail until correctly coded '))
