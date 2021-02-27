# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

def query(returnable, offset = 0, rows = 0):

  limit = """LIMIT        {}, {}""".format(offset, rows) if rows > 0 else ""
  return """
      SELECT 
                M.parent
              , M.name
              , M.idx
              , M.direction
              , M.from_stock
              , M.from_customer
              , M.to_customer
              , M.to_stock
              , M.timestamp
              , CAST(M.timestamp AS DATE) AS move_day
              , M.bapu_id
              , M.if_customer
        FROM `tabReturnable Movement` M
       WHERE parent LIKE '{0}'
         AND parent NOT LIKE ''
    ORDER BY timestamp desc, parent
       {1};
  """.format(returnable, limit)
       # LIMIT 500


def result(query, as_dict = True):
  return frappe.db.sql(query, as_dict=as_dict)

