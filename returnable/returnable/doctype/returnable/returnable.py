# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

import json
import os
import time
import datetime

from operator import attrgetter
from threading import Thread
from frappe.model.document import Document

class Returnable(Document):
  pass

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)

SUCIOS = 'Envases IB Sucios - LSSA'
LLENOS = 'Envases IB Llenos - LSSA'
ERRORS = 'Envases Con Error'

def LG(txt):
  filename = '/dev/shm/erpnext_log/results.log'

  if os.path.exists(filename):
      append_write = 'a' # append if already exists
  else:
      append_write = 'w' # make a new file if not

  logfile = open(filename,append_write)
  logfile.write(txt + "\n")
  logfile.close()

def getQryReturnableMovements(returnable):
  return """
      SELECT parent, name, idx, direction, from_stock, from_customer, to_customer, to_stock, timestamp, bapu_id, if_customer
        FROM `tabReturnable Movement` M
       WHERE 
             parent = '{0}'
         -- AND modified > '2015-12-31 23:12:52.000000'
    ORDER BY parent, creation
  """.format(returnable)

def getQryReturnablesIds():
  return """
      SELECT name, coherente
        FROM `tabReturnable` M
        WHERE coherente NOT IN ('Si', 'Descartado')
          -- AND name in ('IBAA255')
    ORDER BY name
       LIMIT 3000
  """

def getQryReturnableAge(returnable):
  return """
      SELECT max(timestamp) as last_move
        FROM `tabReturnable Movement` M
       WHERE parent = '{0}'
  """.format(returnable)


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
    if move.name == newMove.name:
      startRenumbering = True
      newOne.bapu_id = '{0}-1'.format(move.bapu_id)
      newOne.idx = move.idx - typeOfFix[fixType].idx
      newOne.timestamp = move.timestamp - halfTimeGap
      # newOne.timestamp = move.timestamp - datetime.timedelta(microseconds=1)
      newOne.creation = newOne.timestamp
    if startRenumbering:
      move.idx += 1

    # LG('Move :: {0} {1} {2} {3}'.format(idx, move.idx, move.name, startRenumbering))
    idx += 1

  # LG('Last Move :: {0} {1} {2}'.format(idx, returnable.moves[length - 1].idx, returnable.moves[length - 1].name))

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

def installReturnables():

  limit = 25

  returnables = frappe.db.sql(getQryReturnablesIds(), as_dict=True)
  pmv = frappe._dict({ "name": None, "frm": None, "to": None })
  for returnable in returnables:
    nameReturnable = returnable.name

    # if nameReturnable == 'IBAA255':
    #   LG('\n\n\n\n     Returnable :: {0} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n'.format(nameReturnable))
    #   break

    coherent = returnable.coherente

    if itsAnActiveReturnable(returnable):
      LG('\n\nProcessing returnable :: {0} is coherente? <{1}>'.format(nameReturnable, returnable.coherente))
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
    else:
      LG("""  Returnable '{0}' is too old to be worth correcting! ***\n\n""".format(nameReturnable))
      Ret = frappe.get_doc('Returnable', nameReturnable)
      Ret.coherente = 'Descartado'
      Ret.save()
      frappe.db.commit()




@frappe.whitelist()
def install_returnables():
  LG("Starting ... ")

  frappe.enqueue('returnable.returnable.doctype.returnable.returnable.installReturnables', now = True, timeout=60000)
  # enqueue_long_job()

  LG("Finished ... exiting\n##########################################################################################")
  return { "abc": 123 }

