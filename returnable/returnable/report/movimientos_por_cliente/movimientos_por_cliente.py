# Copyright (c) 2013, Warehouseman and contributors
# For license information, please see license.txt

import frappe

def db_query(filters=None):
  query  = """
   SELECT
          DATE(M.timestamp) AS Fecha,
          M.direction AS 'Dirección',
          R.name AS Retornable,
          R.state AS Estado,
          IFNULL(from_customer, to_customer) AS Cliente
     FROM `tabReturnable` R
LEFT JOIN `tabReturnable Movement` M
       ON R.name = M.parent
      AND IFNULL(to_customer, from_customer) != ''
      AND IFNULL(to_customer, from_customer) = '{0}'
    WHERE R.state NOT IN ('Confuso')
      AND M.direction NOT IN ('Stock >> Stock')
      AND M.direction IS NOT NULL
 ORDER BY IFNULL(to_customer, from_customer), timestamp desc, direction
  """.format(filters.customer)

  return [[str(col) for col in row] for row in frappe.db.sql(query)]


def get_columns():
  return [
    # {
    #   "fieldname": "Cliente",
    #   "fieldtype": "Data",
    #   "label": "Cliente",
    #   "width": 250
    # },
    {
      "fieldname": "Fecha",
      "fieldtype": "Date",
      "label": "Fecha",
      "width": 100
    },
    {
      "fieldname": "Direccion",
      "fieldtype": "Data",
      "label": "Dirección",
      "width": 100
    },
    {
      "fieldname": "Retornable",
      "fieldtype": "Data",
      "label": "Retornable",
      "width": 90
    },
    {
      "fieldname": "Estado",
      "fieldtype": "Data",
      "label": "Estado Ahora",
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
