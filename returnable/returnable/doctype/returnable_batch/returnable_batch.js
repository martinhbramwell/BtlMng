// Copyright (c) 2020, Warehouseman and contributors
// For license information, please see license.txt

function setMandatory(frm) {
  const dir = frm.doc.direction;
  frm.set_df_property('to_customer', 'reqd', dir.includes('--> Cust'))
  frm.set_df_property('from_customer', 'reqd', dir.includes('Cust -->'))
  frm.set_df_property('to_stock', 'reqd', dir.includes('--> Stock'))
  frm.set_df_property('from_stock', 'reqd', dir.includes('Stock -->'))

  frm.set_df_property('to_customer', 'hidden', dir.includes('--> Stock'))
  frm.set_df_property('from_customer', 'hidden', dir.includes('Stock -->'))
  frm.set_df_property('to_stock', 'hidden', dir.includes('--> Cust'))
  frm.set_df_property('from_stock', 'hidden', dir.includes('Cust -->'))
}

frappe.ui.form.on('Returnable Batch', {
	setup: function(frm) {
    console.log(`setup ${frm.doc.direction}`);
    setMandatory(frm);
    frm.set_value('timestamp', frappe.datetime.now_datetime());
    frm.set_df_property('timestamp', 'hidden', 0);
    // frm.set_value('timestamp', Date.now());

  },
  onload: function(frm) {
    console.log('onload');
    setMandatory(frm);
  },
  refresh: function(frm) {
    console.log('refresh');
  },
  validate: (frm, cdt, cdn) => {
    console.log(`Validating child ${cdn} (${cdt}):`);
  },
  direction: (frm, cdt, cdn) => {
    console.log(`direction ${cdn} (${cdt}):`);
    setMandatory(frm);
  },
  specify_date: (frm, cdt, cdn) => {
    console.log(`specify_date ${cdn} (${cdt}):  ${frm.doc.specify_date}` );
    console.dir(frappe.datetime);
    frm.set_df_property('timestamp', 'read_only', ! frm.doc.specify_date)
    frm.set_value('timestamp', frappe.datetime.now_datetime());
  }
});
