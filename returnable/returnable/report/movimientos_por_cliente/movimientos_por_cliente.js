// Copyright (c) 2016, Warehouseman and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Movimientos por Cliente"] = {
	"filters": [
    {
      fieldname:"customer",
      label: __("Customer"),
      fieldtype: "Link",
      options: "Customer",
      default: "stapel"
    },
	]
};
