# Copyright (c) 2013, Warehouseman and contributors
# For license information, please see license.txt

import frappe

def db_query(filters=None):
  query = """
      SELECT 
            direction as direccion
          , from_stock as "del_almacen"
          , from_customer as "del_cliente"
          , to_customer as "al_cliente"
          , to_stock as al_almacen
          , DATE(B.timestamp) as fecha
          , bapu_id as bapu_id
        FROM 
            `tabReturnable Batch` B
          , `tabReturnable Batch Item` I 
       WHERE 
             B.name = I.parent
         AND I.bottle = '{0}'
    ORDER BY I.bottle, timestamp desc
  """.format(filters.retornable)

  return [[str(col) for col in row] for row in frappe.db.sql(query)]


def get_columns():
  return [
    {
      "fieldname": "direccion",
      "fieldtype": "Data",
      "label": "Dirección",
      "width": 100
    },
    {
      "fieldname": "del_almacen",
      "fieldtype": "Data",
      "label": "Del Almacén",
      "width": 140
    },
    {
      "fieldname": "del_cliente",
      "fieldtype": "Data",
      "label": "Del Cliente",
      "width": 220
    },
    {
      "fieldname": "al_cliente",
      "fieldtype": "Data",
      "label": "Al Cliente",
      "width": 220
    },
    {
      "fieldname": "al_almacen",
      "fieldtype": "Data",
      "label": "Al Almacén",
      "width": 140
    },
    {
      "fieldname": "fecha",
      "fieldtype": "Date",
      "label": "Fecha",
      "width": 90
    },
    {
      "fieldname": "bapu_id",
      "fieldtype": "Data",
      "label": "ID BAPU",
      "width": 120
    },
  ]


def getData(data, columns):
  # column_names = 
  # print('column_names')
  # print(column_names)
  # print('getData: data')
  # print(data)
  return [ dict(zip([column['fieldname'] for column in columns], row)) for row in data ]


def execute(filters=None):

  columns = get_columns()
  query_result = db_query(filters)
  # print('query_result')
  # print(query_result)

  if query_result is not None:
    # data = get_data(query_result, filters)

    data = getData(query_result, columns)
    # print('data')
    # print(data)

    # query_result = query()
    # data = get_data(query_result, filters)

    return columns, data

  return columns, []
