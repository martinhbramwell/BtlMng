# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

def query(conditions = ''):
  clause = '' if conditions == '' else "AND {}".format(conditions)
  return """
      SELECT
               R.name
             , R.coherente
             , R.last_customer
             , 'Unknown' as location
        FROM `tabReturnable` R
       WHERE R.coherente NOT IN ('Si', 'Descartado')
         {}
    ORDER BY name
  """.format(clause)
       # LIMIT 3000

# def chk():
#   query = """
#       SELECT *
#         FROM `tabReturnable` R
#        WHERE coherente = 'Si'
#   """
#   return frappe.db.sql(query)

def result(query, as_dict):
  return frappe.db.sql(query, as_dict = as_dict)

def lookup(query):
  rows = frappe.db.sql(query, as_dict = True)
  lookup = frappe._dict({})
  for row in rows:
    lookup[row.name] = row

  return lookup



