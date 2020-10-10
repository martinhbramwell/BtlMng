// Copyright (c) 2016, Warehouseman and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Movimientos por Retornable"] = {
	"filters": [
    {
      fieldname:"retornable",
      label: __("Retornable"),
      fieldtype: "Link",
      options: "Returnable",
      default: ""
    },
	]
};
