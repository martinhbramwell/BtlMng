

const fulfilMissingRequirements = ctx => {
    const { inserts, updates } = ctx;
    // console.log(ctx);
    // console.log(`inserts`);
    // console.log(inserts);
    // console.log(`updates`);
    // console.log(updates);

    let msg = "";
    let idxInsert = 0;
    inserts.forEach(item => {
        console.log(`Item : `);
        console.log(item);
        let row = this.frm.add_child('items', item);
        idxInsert += 1;
    });
    this.frm.refresh_field('items');

    if (idxInsert > 0) {
        msg += idxInsert == 1  ?  " 1 row" : ` rows`;
        msg += " added to the table.";
    }

    let idxUpdate = 0;
    console.log(this.frm.doc.items[0]);
    const { items } = this.frm.doc;
    items.forEach(dnItem => {
        const { item_code, qty: currentQty } = dnItem;
        if (updates[item_code]) {
            const { qty: correctQty } = updates[item_code];
            if (currentQty < correctQty) {
                // console.log(`Update Item :  Quantity: Current , Correct `);
                dnItem.qty = correctQty;
                idxUpdate += 1;
            }
        }
    });
    this.frm.refresh_field('items');

    if (idxUpdate > 0) {
        msg += msg.length > 0  ?  " and "  :  "";
        msg += idxUpdate == 1  ?  "1 table row" : ` table rows`;
        msg += " altered.";
    }

    // console.log(`msg`);
    // console.log(msg);
    frappe.msgprint(__(``));
    frappe.validated = (idxUpdate + idxInsert) === 0;

};


const getAccompanimentItemsThenValidateDN = () => {
    const { items: delivery_note_items } = this.frm.doc;
    console.log(this.frm.doc);
    const method = "returnable.returnable.doctype.returnable.delivery_note.getDeliveryNoteAccompanimentItems";
    return { method,
        args: { delivery_note_items },
        callback: insertsAndUpdates => fulfilMissingRequirements(insertsAndUpdates.message)
        // callback: insertsAndUpdates => {
        //     console.log(insertsAndUpdates);
        // }
    };
};

const validate = () => {
    const event = "validate";
    console.log(`##########################->|  |<-###############################`);
    frappe.call(getAccompanimentItemsThenValidateDN());
    // frappe.validated = false;
    // frappe.msgprint(__("Validate curtailed"));
};

const before_submit = () => {
    const event = "before_submit";
    console.log(`##########################->|  |<-###############################`);
    frappe.call(getAccompanimentItemsThenValidateDN());
    // frappe.msgprint(__("Submit curtailed"));
    // frappe.validated = false;
};

frappe.ui.form.on('Delivery Note', { validate, before_submit });

