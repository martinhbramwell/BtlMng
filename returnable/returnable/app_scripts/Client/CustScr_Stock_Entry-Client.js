const CLEAN_ROOM = "cuarto limpio";
const DIRTY_BOTTLES = "envases sucios";
const FILLED_BOTTLES = "envases llenos";
const STOCK_ENTRY_TYPE_MANUFACTURE = "Manufacture";

const makeNewStockEntry = () => {
    console.log(`------ ->| makeNewStockEntry |<- -------`);
    const { work_order } = this.frm.doc;
    console.log(`------ ->| ${work_order} |<- -------`);

    const newRow = frappe.model.get_new_doc("Stock Entry Detail");

    // newRow.parentfield = "items";
    // newRow.parenttype = "Stock Entry";
    // newRow.docstatus = 0;

    newRow.doctype = "Stock Entry Detail";
    newRow.item_code = "FICHA - para envase IB de 5GL";
    newRow.s_warehouse = "Envases IB Sucios - LSSA";
    newRow.t_warehouse = "Envases IB Llenos - LSSA";
    newRow.qty = 1;
    newRow.conversion_factor = 1.0;
    newRow.allow_zero_valuation_rate = 1;
    newRow.serial_no = "No_Existe";

    const seNew = frappe.model.get_new_doc("Stock Entry");
    seNew.stock_entry_type = "Material Transfer";
    seNew.purpose = "Material Transfer";
    // seNew.stock_entry_type = "Manufacture";
    // seNew.purpose = "Manufacture";
    seNew.work_order = work_order;
    // seNew.naming_series = "MAT-STE-.YYYY.-";
    seNew.items = [];
    seNew.items.push(newRow);

    console.log(`* * * New Stock Entry * * * `);
    console.dir(seNew);

    frappe.set_route("Form", "Stock Entry", seNew.name);
};

const startNewStockEntry = ctx => {
    const { doc: D } = this.frm;
    const { items } = D;
    const { inserts, updates, warehouses } = ctx;
//     // console.log(ctx);
    console.log(`Inserts`);
    console.log(inserts);
    console.log(`Updates`);
    console.log(updates);
    console.log(`Warehouses`);
    console.log(warehouses);

    console.log(`### TYPE: ${STOCK_ENTRY_TYPE_MANUFACTURE}, FROM: ${warehouses[CLEAN_ROOM]}, TO: ${warehouses[FILLED_BOTTLES]}`);
    console.log(`### type: ${D.stock_entry_type}, from: ${D.from_warehouse}, to: ${D.to_warehouse}`);
    console.log(`### item`);
    console.dir(items[0]);

    if ( 
           D.stock_entry_type === STOCK_ENTRY_TYPE_MANUFACTURE
        && D.from_warehouse === warehouses[CLEAN_ROOM]
        && D.to_warehouse === warehouses[FILLED_BOTTLES]
    ) {

        // frappe.model.with_doctype("Stock Entry", makeNewStockEntry())

        frappe.msgprint(__("Submit curtailed"));
        frappe.validated = false;
    } else {
        console.log(`Not a special case Stock Entry. No action taken.`);
    }

};

const getAccompanimentItemsThenStartNewStockEntry = () => {
    const doc_type = "Stock Entry";
    const { items: doc_items, work_order } = this.frm.doc;
    const work_order_context = { "work_order": work_order, "purpose": "Manufacture" }
    console.log(work_order_context);
//     // console.log(this.frm.doc);
    const method = "returnable.returnable.doctype.returnable.accompaniment_carrier.getCarrierAccompanimentItems";
    return { method,
        args: { doc_type, doc_items, work_order_context },
        // // callback: insertsUpdatesAndWarehouses => fulfilMissingRequirements(insertsUpdatesAndWarehouses.message)
        callback: insertsUpdatesAndWarehouses => startNewStockEntry(insertsUpdatesAndWarehouses.message)
        // callback: insertsUpdatesAndWarehouses => {
        //     console.dir(insertsUpdatesAndWarehouses);
        // }
    };
};

const on_submit = () => {
    const event = "on_submit";
    console.log(`########################## ->| ${event} |<- ###############################`);
    console.log(`WO : ${this.frm.doc.work_order}`);

    frappe.route_options = {"work_order": this.frm.doc.work_order};
    frappe.set_route("List", "Stock Entry");

    // frappe.validated = false;
    // frappe.msgprint(__("Submit curtailed"));
};

const before_submit = () => {
    const event = "before_submit";
    console.log(`########################## ->| ${event} |<- ###############################`);
    // console.log(`WO : ${this.frm.doc.work_order}`);
    // frappe.route_options = {"work_order": this.frm.doc.work_order};
    // frappe.set_route("List", "Stock Entry");

    frappe.call(getAccompanimentItemsThenStartNewStockEntry());

    // frappe.validated = false;
    // frappe.msgprint(__("Submit curtailed"));
};

const validate = () => {
    const event = "validate";
    console.log(`########################## ->| ${event} |<- ###############################`);

    // frappe.validated = false;
    // frappe.msgprint(__("Validate curtailed"));
};


frappe.ui.form.on('Stock Entry', { before_submit, on_submit, validate });
