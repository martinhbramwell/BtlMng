
// frappe.ui.form.on("Returnable Movement", "direction", function(frm, cdt, cdn) {
//   console.log(`Altered child ${cdn} (${cdt}):`);
// });

// frappe.ui.form.on('Returnable Movement', {
//   // frm passed as the first parameter
//   refresh(frm) {
//     console.log(`Changed direction:`);
//     console.dir(frm);
//   }
// })

frappe.ui.form.on("Returnable Movement", {
  direction: (frm, cdt, cdn) => {
    console.log(`Changed direction:`);
    // const d = locals[cdt][cdn];

    // console.dir(frm);
    // // // required = ! required;
    // // // if ( warehouse === PRIMA ) warehouse = SEDE;
    // // console.log(`Altered child ${cdn} (${cdt}):`);
    // // // console.log(`Field ${d.direction}: ${required}`);
    // // console.log(`Field 'from_stock': ${d.from_stock}`);
    // // // console.dir(frm);
    // // // frm.set_df_property('to_stock', 'reqd', required);
    // // frm.set_value('from_stock', warehouse);
    // cur_frm.set_value('from_stock', warehouse);

  }
});
