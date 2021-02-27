# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import time

from ....utils import  LG


def query(conditions = '', offset = 0, rows = 0):
  limit = """LIMIT        {}, {}""".format(offset, rows) if rows > 0 else ""

  clause = '' if conditions == '' else "AND {}".format(conditions)

  qry =  """
      SELECT 
              B.name
            , B.bapu_id
            , B.direction
            , B.timestamp
            , CAST(B.timestamp AS DATE) AS batch_day
            , B.from_stock
            , B.from_customer
            , B.to_customer
            , B.to_stock
            , B.returnables
            , I.bottle
        FROM `tabReturnable Batch` B, `tabReturnable Batch Item` I
       WHERE I.parent = B.name
         {0}
    ORDER BY B.timestamp desc
       {1};
  """.format(clause, limit)

  # LG("""Query :: {}""".format(qry))     
  return qry

def result(query, as_dict = True):
  return frappe.db.sql(query, as_dict = as_dict)

def lookup():

  lookup = frappe._dict({})

  rowCount = 999999
  rows = 10000
  offset = 0
  while rowCount > 0:
    # LG("offset : {}".format(offset))
    result = frappe.db.sql(query(conditions = "B.timestamp > '2018-12-31'", offset = offset, rows = rows), as_dict = True)
    offset = offset + rows

    for record in result:
      lookup["{}|{}|{}".format(record.bottle, record.batch_day, record.direction)] = record

    # LG("len(result) = {}".format(len(result)))
    rowCount = len(result)

  return lookup



