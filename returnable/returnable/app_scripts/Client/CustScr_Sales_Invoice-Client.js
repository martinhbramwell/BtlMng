frappe.ui.form.on('Sales Invoice', {
    refresh: (frm) => {
        const doc = frm.doc;
        const task = {};

        if (! frm.cscript.einvoice) {
            // console.log("creating 'einvoice' script (=>)");
            frm.cscript.einvoice = (frm, cmd) => {
                frappe.call({
                    method: "electronic_invoice.electronic_invoice.doctype.electronic_invoice.electronic_invoice.electronic_invoice",
                    // method: "erpnext.accounts.doctype.sales_invoice.sales_invoice.electronic_invoice",
                    args: { invoice_id : frm.docname, command : cmd },
                    callback: (resp) => {
                        console.dir(resp);
                        // const response = JSON.parse(resp.responseText);
                        // console.dir(response);
                        frm.reload_doc();
                    }
                });
            };
        }

        if (doc.docstatus > 0 && doc.next_step !== 'Fin') {
            if (doc.accepted_by_revenue_service && doc.authorized_by_revenue_service) {
                task.item = "Mail Authorization to Customer";
                task.cmd = "mail";
            } else if (doc.accepted_by_revenue_service && !doc.authorized_by_revenue_service) {
                task.item = "Verify in Revenue Service";
                task.cmd = "verify";
            } else {
                task.item = "Submit to Revenue Service";
                task.cmd = "submit";
            }
            console.log('Expect "' + task.cmd + '" menu to appear');

            frm.page.add_menu_item(__(task.item), () => {
                frappe.msgprint(task.msg);
                frm.cscript.einvoice(frm, task.cmd);
            });
        }
    }
});
