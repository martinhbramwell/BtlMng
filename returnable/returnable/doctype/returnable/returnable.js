// Copyright (c) 2020, Warehouseman and contributors
// For license information, please see license.txt

function fixMandatory(frm, name) {
  console.log(`Record ${name}`);

  const current_row = frm.fields_dict["moves"].grid.grid_rows_by_docname[name];
  console.dir(current_row);

  // const direction = current_row.columns.direction[0].textContent;
  // console.log(`Current row '${name}' indicates '${direction}'`);

  current_row.toggle_reqd("from_stock", false);
  current_row.toggle_reqd("from_customer", false);
  current_row.toggle_reqd("to_stock", false);
  current_row.toggle_reqd("to_customer", false);

  // current_row.toggle_reqd("from_stock", direction.includes('Stock >'));
  // current_row.toggle_reqd("from_customer", direction.includes('Cust >'));
  // current_row.toggle_reqd("to_stock", direction.includes('> Stock'));
  // current_row.toggle_reqd("to_customer", direction.includes('> Cust'));
}

frappe.ui.form.on('Returnable', {
	// refresh: function(frm, dt, dn) {
 //    console.log(`Refreshed ${dn} (${dt}):  [8]`);
 //    // console.dir(frm);
 //    cur_frm.doc.moves.some(m => {
 //      console.log(`Movement: ${m.direction} :: ${m.from_stock}`);
 //      console.dir(m);
 //    });
 //  },
  validate: (frm, cdt, cdn) => {
    console.log(`Validating child ${cdn} (${cdt}):`);
    frm.fields_dict["moves"].grid.data.forEach(row => fixMandatory(frm, row.name));
  },
  onload: (frm, cdt, cdn) => {
    console.log(`Loading child ${cdn} (${cdt}):`);
    frm.set_query("moves", "items", function() {
        return {
            query: "erpnext.controllers.queries.item_query",
            filters: frm.doc.enquiry_type === "Maintenance" ?
                {"is_service_item": "Yes"} : {"is_sales_item": "Yes"}
        };
    });
  }
});

const PRIMA = 'Materia ARC - LSSA';
const SEDE = 'Sede - LSSA';
let required = 0;
let warehouse = PRIMA;
frappe.ui.form.on("Returnable Movement", {
  direction: (frm, cdt, cdn) => {
    console.log(`Altered child ${cdn} (${cdt}):`);

    const row = locals[cdt][cdn];

    var current_row = frm.fields_dict["moves"].grid.grid_rows_by_docname[row.name];
    console.log(`Current row '${row.name}' indicates 'row.direction'`);

    current_row.toggle_reqd("from_stock", row.direction.includes('Stock >'));
    current_row.toggle_reqd("from_customer", row.direction.includes('Cust >'));
    current_row.toggle_reqd("to_stock", row.direction.includes('> Stock'));
    current_row.toggle_reqd("to_customer", row.direction.includes('> Cust'));
  }
});

frappe.ui.form.on("Delivery Trip", {
  refresh: (frm, cdt, cdn) => {
    console.log(`######################### Delivery Trip => refresh() ${cdn} (${cdt}):`);
    console.dir(frm);
  }
});


