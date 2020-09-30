// Copyright (c) 2016, Warehouseman and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Minimal Script Report with Chart"] = {
  "filters": [
    {
      fieldname: "xAxisField",
      label: "Range Selection Filter",
      fieldtype: "Select",
      options: "15\n30\n45\n60",
      default: 15
    },
  ]
};
