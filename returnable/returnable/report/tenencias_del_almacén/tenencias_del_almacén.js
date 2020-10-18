// Copyright (c) 2016, Warehouseman and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tenencias del Almacén"] = {
	"filters": [
    {
      fieldname:"warehouse",
      label: __("Almacén"),
      fieldtype: "Link",
      options: "Warehouse",
      default: ""
    },
	]
};
