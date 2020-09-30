# Copyright (c) 2013, Warehouseman and contributors
# For license information, please see license.txt

def query():
  return [
    { "xAxisField":  30, "yAxisField": 4156.78 },
    { "xAxisField":  45, "yAxisField": 3908.34 },
    { "xAxisField":  60, "yAxisField": 5632.87 },
    { "xAxisField":  75, "yAxisField": 5698.21 },
    { "xAxisField":  90, "yAxisField": 2321.54 },
    { "xAxisField": 105, "yAxisField": 4446.88 }
  ]

def get_columns():
  return [
    {
      "fieldname": "xAxisField",
      "fieldtype": "Int",
      "label": "X-Axis",
      "width": 100
    },
    {
      "fieldname": "yAxisField",
      "fieldtype": "Currency",
      "label": "Y-Axis",
      "width": 100
    },
  ]

def get_data(data, fltr):
  return [ value for value in data if value["xAxisField"] > int(fltr.xAxisField) ]

def get_chart(data, columns, fltr):
  attributes = [d.get("fieldname") for d in columns]

  dimensions = [
    [
      value.get(attr) for value in data if value["xAxisField"] > int(fltr.xAxisField)
    ] for attr in attributes
  ]

  L = 0
  V = L + 1

  chart = {
    'data': {
      'labels': dimensions[L],
      'datasets': [
        {
          'name': 'Y Value',
        'values': dimensions[V]
        }
      ]
    },
    'isNavigable': 1,
    'type': 'bar'
  }

  return chart

def execute(filters=None):
  query_result = query()

  columns = get_columns()
  data = get_data(query_result, filters)
  message = "Here is a message"
  chart = get_chart(query_result, columns, filters)

  return columns, data, message, chart
