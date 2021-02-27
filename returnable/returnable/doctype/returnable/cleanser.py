# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import sys
import os
import frappe

from ...utils import  LG
from .queries import Returnables
from .queries import ReturnableMovements
from .queries import ReturnableBatchItems

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

def recreateMissingMovmentsAndBatches():
  LG("    recreateMissingMovmentsAndBatches:")

  bottlesOfDays = ReturnableBatchItems.lookup()
  LG("      A bottle of day : \n        {}".format(bottlesOfDays['IBDD721|2019-01-02|Stock >> Cust']))

  bottles = Returnables.lookup(Returnables.query())
  LG("      A bottle : \n        {}".format(bottles['IBDD721']))


  movements = ReturnableMovements.result(ReturnableMovements.query('%', rows= 20000))
  for movement in movements:
    unique = "{}|{}|{}".format(movement.parent, movement.move_day, movement.direction)
    frm = movement.from_stock if movement.from_customer is None else movement.from_customer
    to = movement.to_stock if movement.to_customer is None else movement.to_customer

    if bottles[movement.parent].location == 'Unknown':
      bottles[movement.parent].location = frm
    elif bottles[movement.parent].location != to:
      LG("\n\nFAIL :: {} | On {}, bottle {} moved from {} to {}".format(bottlesOfDays[unique].name, movement.move_day, movement.parent, frm, to))
      return 'Incoherente'

    LG("       {} | On {}, bottle {} moved from {} to {}".format(bottlesOfDays[unique].name, movement.move_day, movement.parent, frm, to))
  return 'Ok'

@frappe.whitelist()
def clean(company = 'Logichem Solutions S. A.'):
  prepareGlobals(company)
  
  rslt = recreateMissingMovmentsAndBatches()

  # LG("Check ::\n     {}".format(Returnables.chk()))

  msg = "\nResult :: {}\n\n\n".format(rslt)
  LG(msg)
  return { "result": msg }


  # bottlesOfDays = ReturnableBatchItems.lookup(ReturnableBatchItems.query())
  # for bottleOfDay in bottlesOfDays:
  #   LG("Bottle Of Day :: {} ==> {}".format(bottleOfDay, bottlesOfDays[bottleOfDay]))



