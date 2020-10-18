# Copyright (c) 2013, Warehouseman and contributors
# For license information, please see license.txt

import frappe

def db_query(filters=None):
  query  = """
    SELECT
          C.Retornable      AS `Retornable`
        , DATE(B.timestamp) AS `Desde`
        , CONCAT("<a href='/desk#Form/Returnable%20Batch/", B.name, "' target='_blank'>", B.name,"</a>") as `Lote`
        , I.name            AS `Item`
        , B.bapu_id         AS `IDBAPU`
      FROM
          `tabReturnable Batch` B
INNER JOIN (
        SELECT Retornable, MAX(Fecha) AS Fecha
          FROM (
               SELECT
                     MAX(M.timestamp) AS Fecha
                   , N.bottle AS Retornable
                   , M.direction AS Direccion
                 FROM
                     `tabReturnable Batch` M
                   , `tabReturnable Batch Item` N
                WHERE N.parent = M.name
                  AND M.docstatus = 1
             GROUP BY Retornable, Direccion
          ) A
        GROUP BY Retornable
      ) C ON C.Fecha = B.timestamp
         , `tabReturnable Batch Item` I
     WHERE
           B.to_stock = '{0}'
       AND I.parent = B.name
       AND C.Retornable = I.bottle
       AND B.docstatus = 1
  ORDER BY Retornable
  """.format(filters.warehouse)

  return [[str(col) for col in row] for row in frappe.db.sql(query)]


def get_columns():
  return [
    {
      "fieldname": "Retornable",
      "fieldtype": "Data",
      "label": "Retornable",
      "width": 90
    },
    {
      "fieldname": "Desde",
      "fieldtype": "Date",
      "label": "Desde",
      "width": 140
    },
    {
      "fieldname": "Lote",
      "fieldtype": "Data",
      "label": "Lote",
      "width": 140
    },
    {
      "fieldname": "Item",
      "fieldtype": "Data",
      "label": "Item",
      "width": 140
    },
    {
      "fieldname": "IDBAPU",
      "fieldtype": "Data",
      "label": "ID BAPU",
      "width": 140
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
