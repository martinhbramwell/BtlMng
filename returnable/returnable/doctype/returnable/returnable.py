# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

import json
import os
import gc
import errno
import time
import datetime
import math  

import pandas as pd


from operator import attrgetter
from threading import Thread
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue

class Returnable(Document):
  pass

class DatetimeEncoder(json.JSONEncoder):
  def default(self, obj):
    try:
      return super().default(obj)
    except TypeError:
      return str(obj)

dateformat = "%Y-%m-%d"


def LG(txt, end = "\n"):
  filename = '/dev/shm/erpnext/result.log'

  if os.path.exists(filename):
    append_write = 'a' # append if already exists
  else:
    try:
      os.makedirs('/dev/shm/erpnext')
    except OSError as e:
      if e.errno != errno.EEXIST:
            raise
    append_write = 'w' # make a new file if not

  logfile = open(filename,append_write)
  logfile.write(txt + end)
  logfile.close()


def getQryReturnableMovements(returnable, offset = 0, rows = 0):

  limit = """LIMIT        {}, {}""".format(offset, rows) if rows > 0 else ""
  return """
      SELECT parent, name, idx, direction, from_stock, from_customer, to_customer, to_stock, timestamp, bapu_id, if_customer
        FROM `tabReturnable Movement` M
       WHERE parent LIKE '{0}'
         AND parent NOT LIKE ''
    ORDER BY parent, creation
       {1};
  """.format(returnable, limit)
       # LIMIT 500


def getQryReturnablesIds():
  return """
      SELECT name, coherente
        FROM `tabReturnable` M
       WHERE coherente NOT IN ('Si', 'Descartado')
          -- AND name in ('IBAA255')
    ORDER BY name
  """
       # LIMIT 3000


def getQryReturnableAge(returnable):
  return """
      SELECT max(timestamp) as last_move
        FROM `tabReturnable Movement` M
       WHERE parent = '{0}'
  """.format(returnable)


def getQryAcquisitions():
  return """
    SELECT acquisition, name FROM `tabReturnable` R
  ;
  """.format()


def getQryDropReturnableMovement(returnable, move):
  return """
      DELETE FROM `tabReturnable Movement`
       WHERE name = '{1}'
         AND parent = '{0}'
         AND parentfield = 'moves'
         AND parenttype = 'Returnable'
  """.format(returnable, move)


def reindexMovements(returnable):
  LG('REINDEX')
  idx = 1
  returnable.moves.sort(key=lambda move: "{0}".format(move.timestamp))
  for move in returnable.moves:
    # LG('{0} {1} {2}'.format(move.timestamp, str(move.idx).rjust(3, '0'), move.name))
    move.idx = idx
    idx += 1

  LG('REINDEXED')
  # LG(json.dumps(returnable.moves, sort_keys=True, indent=4, cls=DatetimeEncoder))


def removeSpuriousMovement(returnable, moveName):
  # pass
  theMove = None
  for move in returnable.moves:
    if move.name == moveName:
      theMove = move

  LG('returnable.remove(theMove = {0})'.format(theMove.name))
  returnable.remove(theMove)
  reindexMovements(returnable)


def reDateMovement(returnable, moveName):
  # pass
  nextMove = None
  theMove = None
  next = 0
  idx = 0
  movIdx = 0
  for move in returnable.moves:
    if next > 1:
      nextMove = move
      next = 0
    if next > 0:
      next += 1
    if move.name == moveName:
      theMove = move
      movIdx = idx
      next = 1
    idx += 1

  oneDay = datetime.timedelta(days=1)
  timeGap = (nextMove.timestamp - theMove.timestamp) 
  halfTimeGap = oneDay if timeGap > oneDay else timeGap / 2

  LG(' {4} ************ Move : {0}. Next move {1} ==> {2} {3}'.format(theMove.name, nextMove.name, nextMove.timestamp, theMove.timestamp, movIdx))
  theMove.timestamp = theMove.timestamp + halfTimeGap
  theMove.creation = theMove.timestamp
  LG(' ************ {0}   ===> {1}'.format(theMove.timestamp, returnable.moves[movIdx].name))
  reindexMovements(returnable)

 # ************ Move : RTN-MOV-000006997. Next move RTN-MOV-000006998 ==> 2016-01-05 12:01:20
 # ************ 2016-01-05 12:01:20


def prepareNewMovement(oldMove, newMove, fixType):
  typeOfFix = frappe._dict({
    'Filling': frappe._dict({ 
      "direction": 'Stock >> Stock', 
      "from_stock": SUCIOS, 
      "to_stock": LLENOS, 
      "from_customer": None, 
      "to_customer": None,
      "idx": 0
    }),
    'Customer Return': frappe._dict({
      "direction": 'Cust >> Stock', 
      "from_stock": None, 
      "to_stock": SUCIOS, 
      "from_customer": oldMove.to_customer,
      "to_customer": None,
      "idx": 0
    }),
    'Customer Receipt': frappe._dict({
      "direction": 'Stock >> Cust', 
      "from_stock": LLENOS,
      "to_stock": None, 
      "from_customer": None, 
      "to_customer": newMove.from_customer,
      "idx": 0
    }),
  })

  # LG("typeOfFix[fixType] {}".format(typeOfFix[fixType]))
  return frappe._dict({
    'direction': typeOfFix[fixType].direction,
    'from_stock': typeOfFix[fixType].from_stock,
    'to_stock': typeOfFix[fixType].to_stock,
    'from_customer': typeOfFix[fixType].from_customer,
    'to_customer': typeOfFix[fixType].to_customer,
    'bapu_id': '',
    'idx': -1,
    'timestamp': None,
    'creation': None
  })


def insertNewMovement(returnable, oldMove, newMove, fixType):
  LG('\ninsertNewMovement\nMove name :: {0}'.format(newMove.name))

  typeOfFix = frappe._dict({
    'Filling': frappe._dict({ 
      "direction": 'Stock >> Stock', 
      "from_stock": SUCIOS, 
      "to_stock": LLENOS, 
      "from_customer": None, 
      "to_customer": None,
      "idx": 0
    }),
    'Customer Return': frappe._dict({
      "direction": 'Cust >> Stock', 
      "from_stock": None, 
      "to_stock": SUCIOS, 
      "from_customer": oldMove.to_customer,
      "to_customer": None,
      "idx": 0
    }),
    'Customer Receipt': frappe._dict({
      "direction": 'Stock >> Cust', 
      "from_stock": LLENOS,
      "to_stock": None, 
      "from_customer": None, 
      "to_customer": newMove.from_customer,
      "idx": 0
    }),
  })

  # print(typeOfFix[fixType])
  returnable.append("moves", {
    'direction': typeOfFix[fixType].direction,
    'from_stock': typeOfFix[fixType].from_stock,
    'to_stock': typeOfFix[fixType].to_stock,
    'from_customer': typeOfFix[fixType].from_customer,
    'to_customer': typeOfFix[fixType].to_customer,
    'bapu_id': '',
    'idx': -1,
    'timestamp': None,
    'creation': None
  })


  oneDay = datetime.timedelta(days=1)
  timeGap = (newMove.timestamp - oldMove.timestamp) 
  halfTimeGap = oneDay if timeGap > oneDay else timeGap / 2
  # LG('?????')
  # LG(json.dumps(oldMove.timestamp, sort_keys=True, indent=4, cls=DatetimeEncoder))
  # LG(json.dumps(newMove.timestamp, sort_keys=True, indent=4, cls=DatetimeEncoder))
  # LG(json.dumps(oneDay, sort_keys=True, indent=4, cls=DatetimeEncoder))
  # LG(json.dumps(timeGap, sort_keys=True, indent=4, cls=DatetimeEncoder))
  # LG(json.dumps(halfTimeGap, sort_keys=True, indent=4, cls=DatetimeEncoder))
  # LG('?????')

  startRenumbering = False
  idx = 0
  length = len(returnable.moves)
  newOne = returnable.moves[length -1]
  while idx < length - 1:
    move = returnable.moves[idx]
    LG("""move.name: {0}, newMove.name {1}""".format(move.name, newMove.name))
    if move.name == newMove.name:
      startRenumbering = True
      newOne.bapu_id = '{0}-1'.format(move.bapu_id)
      newOne.idx = move.idx - typeOfFix[fixType].idx
      newOne.timestamp = move.timestamp - halfTimeGap
      # newOne.timestamp = move.timestamp - datetime.timedelta(microseconds=1)
      newOne.creation = newOne.timestamp
    if startRenumbering:
      move.idx += 1

    LG('Move :: {0} {1} {2} {3}'.format(idx, move.idx, move.name, startRenumbering))
    idx += 1

  LG('Last Move :: {0} {1} {2}'.format(idx, returnable.moves[length - 1].idx, returnable.moves[length - 1].name))


def sorter(elem):
  return "%02d %s" % (elem['age'], elem['name'])


def installReturnablesTester():

  my_list = [
    frappe._dict({'name':'Homer', 'age':39}),
    frappe._dict({'name':'Milhouse', 'age':10}),
    frappe._dict({'name':'Bart', 'age':10})
  ]
  # my_list.sort(key=sorter(elem))
  my_list.sort(key=lambda move: "{0}".format(move.name))
  LG(json.dumps(my_list, sort_keys=True, indent=4, cls=DatetimeEncoder))


def cleanReturnableOnce(returnable):

  nameReturnable = returnable.name
  Ret = frappe.get_doc('Returnable', nameReturnable)
  reindexMovements(Ret)

  if True:
    movements = frappe.db.sql(getQryReturnableMovements(nameReturnable), as_dict=True)
    moves = len(movements)

    step = 0 
    w = 25
    lookAhead = 1
    makeChanges = True
    if moves < 2:
      Ret.coherente = 'Si'
    else:
      for mv in movements:
        mv_f = mv.from_customer if 'Cust >>' in mv.direction else mv.from_stock
        mv_t = mv.to_customer if '>> Cust' in mv.direction else mv.to_stock
        mv_from = mv_f or ''
        mv_to = mv_t or ''
        spcr =' '
        if True:
          if lookAhead < moves:
            ahead = movements[lookAhead]
            # LG("   ===>> Look ahead: {0} vs {1} :: {2} vs {3}".format(lookAhead, moves, mv.name, ahead.name))
            if mv.timestamp == ahead.timestamp and ahead.from_customer == pmv.to_customer:
              reDateMovement(Ret, mv.name)
              LG("\n\n\n*****\n\n\n")
              break

          if step > 0:

            if pmv.to == mv_to and pmv.frm == mv_from:
              spcr ='*'
              if makeChanges:
                removeSpuriousMovement(Ret, mv.name)
                makeChanges = False
                Ret.coherente = 'No'
              else:
                Ret.coherente = 'No'

            elif pmv.to != mv_from:
              spcr ='.'
              if pmv.to == SUCIOS and mv_from == LLENOS:
                if makeChanges:
                  insertNewMovement(Ret, pmv, mv, 'Filling')
                  makeChanges = False
                  # Ret.coherente = 'No'
                else:
                  Ret.coherente = 'No'
              else:
                if pmv.timestamp == mv.timestamp:
                  LG('How to process this? From {0} ({1}) :: Unexpected move from {2} to {3}'.format(mv.name, mv.direction, pmv.to, mv_from))
                  LG('Check id reversing makes more sense'.format(pmv.direction))
                  # if makeChanges: insertNewMovement(Ret, pmv, mv, 'Customer Receipt')
                elif '> Cust' in pmv.direction and mv_from == SUCIOS:
                  LG('Insert a Cust to Sucio move ({0})'.format(pmv.direction))
                  if makeChanges:
                    insertNewMovement(Ret, pmv, mv, 'Customer Return')
                    mv_from = pmv.to_customer
                elif 'Cust >' in mv.direction and pmv.to_stock == LLENOS:
                  LG('Insert a Lleno to Cust move ({0})'.format(pmv.direction))
                  if makeChanges: insertNewMovement(Ret, pmv, mv, 'Customer Receipt')
                elif mv.direction == pmv.direction and pmv.name == mv.name:
                  LG('Delete spurious ({0})'.format(pmv.name))
                  if makeChanges: removeSpuriousMovement(Ret, pmv.name)
                elif mv.direction == pmv.direction and pmv.frm == mv_from:
                  LG('How to process this? From {0} ({1}) :: Unexpected move from {2} to {3}'.format(mv.name, mv.direction, pmv.to, mv_from))
                  LG('Insert a Cust to Sucio move ({0})'.format(pmv.direction))
                  if makeChanges: insertNewMovement(Ret, pmv, mv, 'Customer Return')
                  mv_from = pmv.to_customer
                elif 'Cust >' in mv.direction and mv_from == ERRORS:
                  LG('Delete spurious move ({0})'.format(mv.name))
                  if makeChanges: removeSpuriousMovement(Ret, mv.name)
                elif 'Cust >' in mv.direction and mv_from != SUCIOS:
                  LG('Insert a Llenos to Cust move ({0})'.format(pmv.direction))
                  if makeChanges: insertNewMovement(Ret, pmv, mv, 'Customer Receipt')
                else:
                  LG('HOW TO PROCESS THIS? From {0} ({1}) :: Unexpected move from {2} to {3}'.format(mv.name, mv.direction, pmv.to, mv_from))
                  # From Cust >> Stock :: Sofía Lira to Envases Con Error

                Ret.coherente = 'No'
                makeChanges = False

            else:
              if makeChanges: Ret.coherente = 'Si'
        # else:
        #   if lookAhead < moves:
        #     ahead = movements[lookAhead]
        #     LG("   ===>> Look ahead: {0} vs {1} :: {2} vs {3}".format(lookAhead, moves, mv.name, ahead.name))
        #     if ahead.timestamp == mv.timestamp and ahead.from_customer == pmv.to_customer:
        #       mv.timestamp += datetime.timedelta(seconds=1)
        #       LG("\n\n\n*****\n\n\n")

        LG("{0} {1} : [{2}] {3} {4} {5} {6} {7}".format(
          mv.parent,
          str(mv.idx).rjust(3, '0'),
          mv.name,
          mv.timestamp,
          mv.direction.ljust(14, ' '),
          ''.ljust(step, spcr),
          mv_from[:w].ljust(w, ' '),
          mv_to[:w].ljust(w, ' '),
        ))

        pmv = mv
        pmv["to"] = mv_to
        pmv["frm"] = mv_from

        step += w + 1
        lookAhead += 1

  Ret.save()
  frappe.db.commit()
  return Ret.coherente
  # time.sleep(1)


def itsAnActiveReturnable(returnable):
  cutOff = '2016-09-01'
  cutOffDate = datetime.datetime.strptime(cutOff, '%Y-%m-%d')
  returnableAge = frappe.db.sql(getQryReturnableAge(returnable.name), as_dict=True)

  lastMove = returnableAge[0].last_move
  stillActive = False if lastMove is None else lastMove > cutOffDate
  
  LG("""Last move : '{0}'.  Cut off date : '{1}'. Is an Active returnable? {2}""".format(lastMove, cutOffDate, stillActive))
  # LG(json.dumps(returnableAge[0].last_move, sort_keys=True, indent=4, cls=DatetimeEncoder))
  return stillActive


def insertInitialRealignmentStep(move, fixType):

  LG("""  - Returnable: {0}. Move: {1}. BAPU ID: {2}. Batch Cnt: {3} {4}""".format(
    move.name,
    move.direction,
    move.bapu_id,
    move.returnables,
    move.timestamp,
  ))


  returnable = frappe.get_doc('Returnable', move.name)
  newMove = returnable.moves[0]
  oldMove = frappe._dict({ "to_customer": None, "from_customer": None })
  theMove = prepareNewMovement(oldMove, newMove, fixType)
  theMove.timestamp = newMove.timestamp - datetime.timedelta(hours=1)
  # print(theMove)
  returnable.append("moves", theMove)

  reindexMovements(returnable)
  returnable.save()


def insertInitialRealignmentSteps(movements, fixType):
  for move in movements:
    insertInitialRealignmentStep(move, fixType)
  frappe.db.commit()

onlyStockStock = "'Cust >> Stock', 'Cust >> Cust', 'Stock >> Cust'"
onlyCustStock = "'Stock >> Stock', 'Cust >> Cust', 'Stock >> Cust'"
onlyStockCust = "'Cust >> Stock', 'Stock >> Stock', 'Cust >> Cust'"
onlyCustCust = "'Cust >> Stock', 'Stock >> Stock', 'Stock >> Cust'"

def alignAllInitialMoves():

  LG("""Realigning all initial moves""")

  movements = frappe.db.sql(getQryIndexedReturnableMovements(1, 0, 999999, onlyCustStock), as_dict=True)
  LG("""\nInserting a fake DELIVERY step for each bottle that seems to
              begin life with return from a customer.
        'Stock >> Cust' to each of {0} returnables.""".format(len(movements)))
  insertInitialRealignmentSteps(movements, 'Customer Receipt')

  # LG(getQryIndexedReturnableMovements(1, 0, 999999, onlyStockCust))
  movements = frappe.db.sql(getQryIndexedReturnableMovements(1, 0, 999999, onlyStockCust), as_dict=True)
  LG("""\nInserting a fake REFILL step for each bottle that seems to
              begin life with delivery to a customer.
        'Stock >> Stock' to each of {0} returnables.""".format(len(movements)))
  insertInitialRealignmentSteps(movements, 'Filling')

  LG("""Religned initial moves""")


def cleanReturnables():

  limit = 50

  LG('Getting unprocessed returnables')
  returnables = frappe.db.sql(getQryReturnablesIds(), as_dict=True)
  pmv = frappe._dict({ "name": None, "frm": None, "to": None })
  active = 0;
  condemned = 0;
  for returnable in returnables:
    nameReturnable = returnable.name
    LG('Returnable :: {0} '.format(nameReturnable))

    # if nameReturnable == 'IBAA255':
    #   LG('\n\n\n\n     Returnable :: {0} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n'.format(nameReturnable))
    #   break

    coherent = returnable.coherente

    if itsAnActiveReturnable(returnable):
      LG('\n\nProcessing returnable :: {0} is coherente? <{1}>'.format(nameReturnable, coherent))
      count = 1
      while count < limit + 1 and coherent != 'Si':
        coherent = cleanReturnableOnce(returnable)
        LG('Returnable :: {0} Pass #{1} Coherent? {2}\n\n'.format(nameReturnable, count, coherent))
        count += 1

      if count < limit + 1:
        LG(' Returnable :: {0} COMPLETE!\n\n'.format(nameReturnable))
      else:
        LG(' *** Failed after {0} *** Returnable :: {1} Coherent? {2}\n\n'.format(limit, nameReturnable, coherent))
        break
      active += 1
    else:
      LG("""  Returnable '{0}' is too old to be worth correcting! ***\n\n""".format(nameReturnable))
      Ret = frappe.get_doc('Returnable', nameReturnable)
      Ret.coherente = 'Descartado'
      Ret.save()
      frappe.db.commit()
      condemned += 1;


  LG('Processed {} active and {} inactivereturnables'.format(active, condemned))


def custStock(movement):
  rtrn = {
   "frm": "{} - {}".format(movement.from_customer, ABBR_COMPANY),
    "to": movement.to_stock
  }
  # LG("""Regreso movement is from {0} to {1}.""".format(rtrn["frm"], rtrn["to"]))
  return rtrn


def custCust(movement):
  rtrn = {
   "frm": "{} - {}".format(movement.from_customer, ABBR_COMPANY),
    "to": "{} - {}".format(movement.to_customer, ABBR_COMPANY)
  }
  # LG("""Customer trade is from {0} to {1}.""".format(rtrn["frm"], rtrn["to"]))
  return rtrn


def stockStock(movement):
  rtrn = {
    "frm": movement.from_stock,
     "to": movement.to_stock
  }
  # LG("""Relleno movement is from {0} to {1}.""".format(rtrn["frm"], rtrn["to"]))
  return rtrn


def stockCust(movement):
  rtrn = {
    "frm": movement.from_stock,
    "to": "{} - {}".format(movement.to_customer, ABBR_COMPANY)
  }
  # LG("""Entrega movement is from {0} to {1}.""".format(rtrn["frm"], rtrn["to"]))
  return rtrn

    # if "Cust >" in movement.direction:
    # elif "> Cust" in movement.direction:
    #   LG("""Entrega movement is from {0} to {1}.""".format(movement.direction, movement.name))
    # else:
    #   LG("""Relleno movement is from {0} to {1}.""".format(movement.from_stock, movement.to_stock))


directions = {
  "Cust >> Stock": custStock,
  "Cust >> Cust": custCust,
  "Stock >> Cust": stockCust,
  "Stock >> Stock": stockStock
}

def getWarehouses(batch):
  ret = frappe._dict({
    "F": directions[batch.direction](batch)["frm"],
    "T": directions[batch.direction](batch)["to"],
  })
  getWarehouse(ret.F)
  getWarehouse(ret.T)
  return ret


def getQryIndexedReturnableMovements(index, offset = 0, rows = 0, direction = "'Cust >> Cust'"):
  return """
      SELECT 
             R.name
           , M.name as movement
           , M.idx
           , M.timestamp
           , M.transferred
           , M.direction
           , M.from_stock
           , M.from_customer
           , M.to_customer
           , M.to_stock
           , M.bapu_id
          -- , B.flag as flagged
           , B.name as batch
           , B.returnables
        FROM `tabReturnable` R
  INNER JOIN `tabReturnable Movement` M
              ON M.parent = R.name
   LEFT JOIN `tabReturnable Batch` B
              ON B.bapu_id = M.bapu_id
       WHERE R.coherente = 'Si'
         AND M.idx = {0}
         AND M.direction NOT IN ({3})
         -- AND R.name like 'CLAA%'
         -- AND R.name like 'CLCC%'
         -- AND R.name like 'IBAA%'
         -- AND R.name like 'IBCC%'
         -- AND R.name like 'IBDD%'
         -- AND R.name like 'IBEE%'
    ORDER BY R.name, M.idx
         LIMIT {1}, {2};
  """.format(index, offset, rows, direction)
       # LIMIT 500
# | CLAA |       21 |
# | CLCC |        4 |
# | IBAA |      978 |
# | IBCC |      995 |
# | IBDD |      999 |
# | IBEE |       90 |


def insert_new_stock_entry(move, batch_name):
  
  serial_no = None
  wh = getWarehouses(move)
  LG("""  -- From: {0}: To: {1} Batch: {2} Mvmnt: {3} Dir: {4} Bapu: {5}""".format(
     wh.F, wh.T, move.batch, move.movement, move.direction, move.bapu_id
  ))
  items_moved = None
  batch = None
  LG('A')
  movement = frappe.get_doc('Returnable Movement', move.movement)
  # ts = datetime.datetime.strptime(move.timestamp, "%Y-%m-%d %H:%M:%S.%f")
  ts = move.timestamp
  dt = ts.date()
  tm = ts.time()


  LG('B')
  if batch_name is not None:
    # LG("""  -- Batch: {0} BAPU ID: {1}""".format(move.batch, move.bapu_id))
    batch = frappe.get_doc('Returnable Batch', batch_name)
    items_moved = '\n'.join(item.bottle for item in batch.bottles_moved)
    item_count = batch.returnables
    # LG("""  -- items_moved: {0}\n{1}""".format(items_moved, batch.returnables))
  else:
    # LG("""  -- ID: {0}""".format(move.name))
    items_moved = move.name
    item_count = 1

  LG('C')
  se = {
    "doctype": "Stock Entry",
    "stock_entry_type": "Material Transfer",
    "from_warehouse": wh.F,
    "to_warehouse": wh.T,
    "posting_date": dt,
    "posting_time": tm,
    "docstatus": 0,
    "remarks": '{ "direction": {0}, "bapu_id": "{1}" }'.format(move.direction, move.bapu_id),
    "items": [ {
        "item_code": "Envase de 5GL Iridium Blue",
        "qty": item_count,
        "serial_no": items_moved,
      }
    ]
  }

  LG("Stock Entry : {0} Mvmnt : {1}".format(se, movement.name)) # ed9fedc0f1

  stockEntry = frappe.get_doc(se)
  LG('D')
  movement.transferred = 1
  movement.docstatus = 1
  if batch is not None:
    batch.flag = 1
    batch.docstatus = 1
    batch.save()

  movement.save()
  stockEntry.save()
  frappe.db.commit()
  LG('D')


def processStep(movements):
  direction = set()
  for move in movements:
    direction.add(move.direction)
    # LG("""  - Move: {0}. BAPU ID: {1}. Dir: {2}""".format(move.name, move.bapu_id, move.direction))

  msg = """  - Directions: {0}. """.format(direction)
  if len(direction) > 1:
    LG("""Inconsistent {}""".format(msg))
    return 

  for move in movements:
    LG("""\nBottle: {0}. """.format(move.name))
    # LG("""  - Bottle: {0}. Flg: {1}. Dir: {2}. BAPU ID: {3}. Cnt: {4}""".format(move.name, move.flag, move.direction, move.bapu_id, move.returnables))
    whseFrom = directions[move.direction](move)["frm"]
    whseTo = directions[move.direction](move)["to"]

    if move.transferred > 0:
      LG("""Corresponding movement, '{}', has been processed already. """.format(
        move.movement
      ))
    else:
      if move.returnables is None:
        LG("""No corresponding batch. Making a single Material Transfer ({0}) for {1} ({2} => {3}).""".format(move.direction, move.name, whseFrom, whseTo))
        insert_new_stock_entry(move, None)
      elif move.returnables > 1:
        LG("""Batch, '{0}', needs to be processed.  Making a combined Material Transfer ({1}) for {2} bottles ({4} => {5}).""".format(
          move.batch, move.direction, move.returnables, move.name, whseFrom, whseTo
        ))
        insert_new_stock_entry(move, move.batch)
      elif move.returnables > 0:
        LG("""Batch, '{0}', needs to be processed.  Making a single Material Transfer ({1}) for {2} ({3} => {4})""".format(
          move.batch, move.direction, move.name, whseFrom, whseTo
        ))
        insert_new_stock_entry(move, None)
      else:
        LG(""" \n\n\n $$$$$$$$$$$$$$$$$$ ERROR $$$$$$$$$$$$$$$$$$$$\n    - Bottle: {0}. Flg: {1}. Dir: {2}. BAPU ID: {3}. Cnt: {4}""".format(
          move.name, move.flag, move.direction, move.bapu_id, move.returnables
        ))





movementEnds = frappe._dict({
  'Cust >> Stock': { 'F': 'Donde Cliente', 'T': 'Sucios' },
  'Stock >> Stock': { 'F': 'Sucios', 'T': 'Llenos' },
  'Stock >> Cust': { 'F': 'Llenos', 'T': 'Donde Cliente' }
})









def prepareGlobals(company):
  global NAME_COMPANY
  global ABBR_COMPANY
  global SUCIOS
  global LLENOS
  global ROTOS
  global ERRORS
  global EXISTING_LOCATIONS

  theCompany = frappe.get_doc('Company', company)
  NAME_COMPANY = theCompany.company_name
  ABBR_COMPANY = theCompany.abbr

  SUCIOS = "Envases IB Sucios - {}".format(ABBR_COMPANY)
  LLENOS = "Envases IB Llenos - {}".format(ABBR_COMPANY)
  ROTOS = "Envases IB Rotos - {}".format(ABBR_COMPANY)
  ERRORS = "Envases Con Error"

  EXISTING_LOCATIONS = set({ SUCIOS, LLENOS, ROTOS })


def getInitialAcquisitionSerialNumbers():
  serialNumbersPerAcquisitions = frappe._dict()

  LG("Getting initial acquisition serial numbers.")
  acquisitions = frappe.db.sql(getQryAcquisitions(), as_dict=False)
  cnt = 0
  for acquisition in acquisitions:
    if acquisition[0] is not None:
      acquisitionDate = acquisition[0].strftime(dateformat)
      acquisitionId = acquisition[1]
      if acquisitionDate in serialNumbersPerAcquisitions:
        serialNumbersPerAcquisitions[acquisitionDate].append(acquisitionId)
      else:
        serialNumbersPerAcquisitions[acquisitionDate] = [acquisitionId]
    cnt += 1

  LG("Got {} initial acquisition serial numbers.".format(cnt))
  return serialNumbersPerAcquisitions


def makeInitialAcquisitions():
  LG("Creating Material Receipts for Serial Numbered containers.")

  serialNumbersPerAcquisitions = getInitialAcquisitionSerialNumbers()

  cnt = 0
  for date in serialNumbersPerAcquisitions:
    se = {
      "doctype": "Stock Entry",
      "docstatus": 0,
      "to_warehouse": "Envases IB Sucios - LSSA",
      "posting_date": date,
      "posting_time": "09:00:00.000000",
      "set_posting_time": 1,
      "stock_entry_type": "Material Receipt",
      "items": [
        {
          "qty": len(serialNumbersPerAcquisitions[date]),
          "item_code": "Envase de 5GL Iridium Blue",
          "serial_no": ",".join(serialNumbersPerAcquisitions[date])
        }
      ]
    }

    stockEntry = frappe.get_doc(se)
    LG("{} :: {}".format(stockEntry.posting_date, stockEntry.items[0].qty), end = ' ... ')
    try:
      LG("Saving", end = ' ... ')
      stockEntry.save()
      SE = frappe.get_last_doc('Stock Entry')
      LG("Submitting {} ".format(SE.name), end = ' ... ')
      # SE.run_method('submit')
      SE.submit()
      LG("Done")
    except:
      LG("FAILED")

    cnt += 1

  LG("All Done")

  frappe.db.commit()
  LG("Created {} Material Receipts for Serial Numbered containers.".format(cnt))
  

def getQryBatchesOfDay(ctx):
  # LG("""{0} < x < {1}""".format(ctx.begin, ctx.end))
  return """
       SELECT
            R.name
          , R.bapu_id
          , R.timestamp
          , R.direction
          , R.from_stock
          , R.from_customer
          , R.to_customer
          , R.to_stock
          , R.returnables
         FROM `tabReturnable Batch` R 
        WHERE timestamp BETWEEN "{0}" AND "{1}"
     ORDER BY timestamp
  """.format(ctx.begin, ctx.end)


def getQryBatchItem(ctx):
  # LG("""{0} < x < {1}""".format(ctx.begin, ctx.end))
  return """
    SELECT bottle
      FROM `tabReturnable Batch Item` R
     WHERE parent = "{}"
     ;
  """.format(ctx.batch)


def createStockLocation(ctx):
  location = ctx.name
  warehouse_name = ctx.warehouse_name
  warehouse = None
  if location not in EXISTING_LOCATIONS:
    try:
      # LG("""*** Seeking : {}""".format(location), end = ' ... ')
      warehouse = frappe.get_doc("Warehouse", location)
      # LG("Found :: {}".format(warehouse.name))
    except Exception as errFind:
      try:
        # LG("""Creating : {}""".format(location), end = ' ... ')
        warehouse = frappe.get_doc({
            "name": location,
            "doctype": "Warehouse",
            "parent_warehouse": "Envases IB Custodia del Cliente - {}".format(ABBR_COMPANY),
            "is_group": 0,
            "company": NAME_COMPANY,
            "account": "2.1.8.01 - Inventario Entrante No Facturado - {}".format(ABBR_COMPANY),
            "warehouse_type": "Consignado",
            "warehouse_name": warehouse_name
          },
        )
        warehouse.insert()
        warehouse.submit()
        WH = frappe.get_last_doc('Warehouse')

        # LG("Created warehouse :: {}".format(WH.name))
      except Exception as errCreate:
        LG("""  Caught error: {}""".format(errCreate))

    EXISTING_LOCATIONS.add(location)
  # else:
  #   LG("""*** Existing : {}""".format(location))

  # LG("""Have stock Location: {}""".format(location))
  return location


def getWarehouse(warehouse_name):
  context = frappe._dict({
    "warehouse_name": warehouse_name,
    "name": "{} - {}".format(warehouse_name, ABBR_COMPANY)
  })
  # LG("Get warehouse for :: {}".format(context))
  return createStockLocation(context)


def createStockEntry(se):
  LG("        Stock Entry.\n          {}""".format(se));
  stockEntry = frappe.get_doc(se)
  stockEntry.insert()
  stockEntry.submit()
  SE = frappe.get_last_doc('Stock Entry')
  return SE


def CustomerToStockBatch(ctx):
  LG("""      Customer Return Batch.\n        {}\n        {}""".format(ctx.batch, ctx.batchItems));


def CustomerToCustomerBatch(ctx):
  LG("      Customer To Customer Exchange.\n        {}\n        {}""".format(ctx.batch, ctx.batchItems));


def StockToCustomerBatch(ctx):
  LG("      Customer Delivery Batch #{} to {} [{}]""".format(ctx.batch.bapu_id, ctx.batch.to_customer, ctx.batchItems));

  date = ctx.batch.timestamp.strftime('%Y-%m-%d')
  time = ctx.batch.timestamp.strftime('%H:%M:%S.000000')

  customerConsignment = getWarehouse(ctx.batch.to_customer)
  # LG("          Customer Consignment :: {}""".format(customerConsignment));

  se = {
    "doctype": "Stock Entry",
    "docstatus": 1,
    "stock_entry_type": "Material Transfer",
    "posting_date": date,
    "posting_time": time,
    "set_posting_time": 1,
    "items": [
      {
        "qty": len(ctx.batchItems),
        "item_code": "Envase de 5GL Iridium Blue",
        "s_warehouse": LLENOS,
        "t_warehouse": customerConsignment,
        "serial_no": ','.join(ctx.batchItems)
      }
    ]
  }

  SE = createStockEntry(se)
  LG("          Created Stock Entry :: {}""".format(SE.name));


def StockToStockBatch(ctx):
  LG("      Stock To Stock Batch Transfer.\n        {}\n        {}""".format(ctx.batch, ctx.batchItems));
  

batchTransfer = {
  "Cust >> Stock": CustomerToStockBatch,
  "Cust >> Cust": CustomerToCustomerBatch,
  "Stock >> Cust": StockToCustomerBatch,
  # "Stock >> Cust": CustomerToStockBatch,
  "Stock >> Stock": StockToStockBatch
}



def iterateReturnableBatches():
  LG("Iterating returnable batches by date.");
  # startDate = '2015-12-31'
  startDate = pd.to_datetime('2015-12-30')
  endDate = pd.to_datetime('2016-01-03')
  # endDate = pd.to_datetime("now") + pd.to_timedelta(1, unit='d')
  possibleDates = pd.date_range(start=startDate, end=endDate, freq='D')
  for idx, val in enumerate(possibleDates):
    if idx > 0:
      context = frappe._dict({
        "begin": possibleDates[idx-1],
        "end": val - pd.to_timedelta(1, unit='s')
      })
      # LG(getQryBatchesOfDay(context))
      LG("\n {} ---------------------------------------".format(val))
      batches = frappe.db.sql(getQryBatchesOfDay(context), as_dict=True)
      if len(batches) > 0:
        # LG("   {}".format(batches))
        # LG("   ---------")
        for batch in batches:
          # LG("    {} :: {}".format(batch.name, batch.direction))
          items = frappe.db.sql(getQryBatchItem(frappe._dict({ "batch": batch.name })), as_dict=False)
          spec = frappe._dict({
            "batch": batch,
            "batchItems": list(item[0] for item in items)
          })
          # LG("                       Items :: {}".format(spec.batchItems))
          batchTransfer[batch.direction](spec)




@frappe.whitelist()
def installReturnables(company):
  # LG("Getting values for company: {}".format(company))
  prepareGlobals(company)

  cleanReturnables()
  alignAllInitialMoves()

  makeInitialAcquisitions()

  return "Installed Returnables";




# ############################################################################# #


def checkSequentialIntegrity():
  LG("""Returnables:
     """)
  returnables = frappe._dict({})
  result = frappe.db.sql("SELECT code, 'Sucios' as state FROM `tabReturnable` R WHERE R.coherente = 'Si'")
  for row in result:
    returnables[row[0]] = row[1]


  
  moves = frappe.db.sql("""
    SELECT COUNT(*) as moves
      FROM `tabReturnable` R, `tabReturnable Movement` M
     WHERE R.coherente = 'Si'
       AND R.name = M.parent
      """, as_dict=True)
  # moves = frappe.db.sql("SELECT COUNT(*) as moves FROM Movements", as_dict=True)
  loopGroup = round(math.sqrt(moves[0].moves))
  # LG("loopGroup :: {}".format(loopGroup))

  select = """SELECT 
                    M.parent as returnable
                  , M.direction as move
                  , M.timestamp as time
                  , R.coherente
                FROM `tabReturnable` R, `tabReturnable Movement` M
               WHERE R.coherente = 'Si'
                 AND R.name = M.parent
            ORDER BY M.timestamp
               LIMIT"""
  # select = """SELECT parent, direction FROM Movements LIMIT"""
  groupCount = 0
  fullCount = 0
  trap = 400
  mismatch = False
  while True:
    sql = "{} {}, {}".format(select, groupCount, loopGroup)
    # LG(sql)

    moves = frappe.db.sql(sql, as_dict=True)
    limit = len(moves)
    for MV in moves:
      lastMoveAt = returnables[MV.returnable]
      thisMoveFrom = movementEnds[MV.move]['F']
      thisMoveTo = movementEnds[MV.move]['T']
      matched = "OK" if lastMoveAt == thisMoveFrom else " * * Mismatch * * "
      # LG(" {} |  '{}'  vs  '{}'   ==> {}".format(returnable, lastMoveAt, thisMoveFrom, matched))
      LG("{0:06d} ({1} :: {2}) {3} |  '{4}'  vs  '{5}'   ==> {6}".format(fullCount, MV.id, MV.time, MV.returnable, lastMoveAt, thisMoveFrom, matched))

      if lastMoveAt != thisMoveFrom:
        LG("***  Movement mismatch  ***")
        mismatch = True
        break

      returnables[MV.returnable] = thisMoveTo
      fullCount += 1

    if mismatch:
      break

    if limit != loopGroup:
      LG("***  Reached end of data  ***")
      break

    groupCount += loopGroup

    if trap < 1:
      LG("***  TRAP SPRUNG  ***")
      break
    trap -= 1

  rslt = loopGroup

  # for returnable in returnables:
  #   LG("{} : '{}'".format(returnable, returnables[returnable]))

  
  LG("""~~~~~~~~~~~~~~~~~~~  Done  ~~~~~~~~~~~~~~~~~~""")
  return "Tested : {}".format(rslt);


def deleteMovementRange(ctx):
  qry = """
    SELECT R.name, M.idx, M.name, R.fills, R.last_out, R.last_move, R.last_customer, R.times_out
      FROM `tabReturnable` R, `tabReturnable Movement` M
     WHERE R.name = M.parent AND R.name = '{0}' AND M.idx BETWEEN '{1}' AND '{2}'
  ORDER BY M.idx
  """.format(ctx.name, ctx.first, ctx.last)
  rslt = frappe.db.sql(qry)
  ids = []
  for row in rslt:
    # LG("{}".format(row[2]))
    ids.append(row[2])

  badMoves = "'{}'".format("', '".join(ids))
  # LG(badMoves)

  dlt = """DELETE FROM `tabReturnable Movement` WHERE name IN ({0})""".format(badMoves)
  LG(dlt)
  resp = frappe.db.sql(dlt)

  Ret = frappe.get_doc('Returnable', ctx.name)
  Ret.coherente = 'No'
  reindexMovements(Ret)
  Ret.save()

  return len(resp)


def ensureSequentialIntegrity():
  # anomalousReturnables = [
  #   {"name": "IBAA592", "first": 1, "last": 1}
  # ]

  # for returnable in anomalousReturnables:
  #   count = deleteMovementRange(frappe._dict(anomalousReturnables[0]))

  # alignAllInitialMoves()

  checkSequentialIntegrity()


def quickTest(company):
  prepareGlobals(company)
  LG("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nQuick Test :: >{}<""".format(ABBR_COMPANY))

  ensureSequentialIntegrity()

  # # task = "del"
  # # task = "align"
  # task = "confirm"
  # if task == "del":


  #   anomalousReturnables = [
  #     {"name": "IBAA592", "first": 1, "last": 1}
  #   ]

  #   for returnable in anomalousReturnables:
  #     count = deleteMovementRange(frappe._dict(anomalousReturnables[0]))
  #     # specs = cleanReturnableOnce(frappe._dict(returnable))

  # elif task == "align":
  #   # cleanReturnables()
  #   alignAllInitialMoves()

  #   # # LG('???? {}'.format(getQryReturnableMovements("IBAA967")))
  #   return "Cleaned returnables";
  # else:
  #   checkSequentialIntegrity()


@frappe.whitelist()
def tester(company):


  # return { "result": { "name": NAME_COMPANY, "abbr": ABBR_COMPANY, "warehouses": { "Empties": SUCIOS, "Filled": LLENOS } } }

  prepareGlobals(company)
  test = 2
  if test == 1:
    LG("Mapping production batches ... ")
    LG("Mapped  production batches ... exiting\n#######################################################")
    return { "result": "Mapped  production batches" }
  elif test == 2:

    LG("Enqueuing Quick Test")
    msg = quickTest(company)
    return { "result": msg }

  elif test == 3:
    LG("\n\n\nEnqueuing Quick Test")
    fpath = '/opt/docTypeHandlers/BAPU/invoices'
    for filename in os.listdir(fpath):
      if filename.endswith(".json"): 
        fname = "{0}/{1}".format(fpath, filename)
        LG("File {}".format(fname))
        with open(fname) as json_invoice:
          inv = json.load(json_invoice)
          LG("bapu_id : {}".format(inv['data']['seqib']))

    return { "result": "Enqueued Quick Test." }
  elif test == 4:
    LG("Enqueuing Quick Test #4")
    # iterateReturnableBatches()
    return { "result": "Enqueued Quick Test #4." }
  elif test == 5:
    LG("Enqueuing Quick Test #5")
    batch = frappe._dict({ "to_customer": "Brewster" })
    ctx = frappe._dict({ "batch": batch })
    LG("Context :: {}".format(ctx.batch.to_customer))
    customerConsignment = getWarehouse(ctx.batch.to_customer)
    LG("          Customer Consignment :: {}""".format(customerConsignment));
    return { "result": ctx }
  else:
    LG("Find warehouse ...")
    try:
      warehouse = frappe.get_doc("Warehouse", "Marco Lamar - {}".format(ABBR_COMPANY))
    except Exception as errFind:
      LG(errFind)
    LG(warehouse.name)
    ts = "2019-06-09 16:41:36.000000"

    ts = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
    dt = ts.date()
    tm = ts.time()
    LG("dt : {}, tm : {}".format(dt, tm))
    return { "result": warehouse.name }

