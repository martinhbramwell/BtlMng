// Copyright (c) 2022, Warehouseman and contributors
// For license information, please see license.txt



// const fillCustomerReturnablesChildTable = (ctx) => {
//     const { frm } = this;
//     const { lookup } = frm.doc;
//     const { message: customerOfSerialNumber } = ctx;
//     console.log("customerOfSerialNumber");
//     console.log(customerOfSerialNumber);

//     customerOfSerialNumber.forEach(function (row) {
//         const { serial_number, customer } = row;
//         console.log(`sn: ${serial_number},  cust: ${customer}`);

//         let color = "red";
//         let icon = "fa-times";
//         if (lookup[serial_number]) {
//             if (lookup[serial_number].includes(customer)) {
//                 color = "green";
//                 icon = "fa-check";
//             }
//         }
//         frm.add_child('customer_returnables', {
//             "serial_number": serial_number,
//             // "customer": customer,
//             "consignment": lookup[serial_number],
//             // "found": `<i class=\"fa ${icon}\"  style=\"color:${color}\"></i>`
//         });
//     });

//     frm.refresh_field('customer_returnables')

//     frm.fields_dict.customer_returnables.grid.grid_rows.forEach(row => {
//         row.select(true);
//         row.refresh_check();
//     });
//     // this.frm.add_child('customer_returnables', { serial_number: "abc", customer: "zyz" });
//     // this.frm.add_child('customer_returnables', { serial_number: "mno", customer: "pqr" });
//     // this.frm.refresh_field('customer_returnables')
// }

// const getRouteCustomersExistingReturnables = () => {
//     const { delivery_trip } = this.frm.doc;
//     const method = "returnable.returnable.doctype.returnables_batch_transfers.returnables_batch_transfers.getRouteCustomersExistingReturnables";
// 		frappe.call({ method,
//         args: { delivery_trip },
//         callback: resp => fillCustomerReturnablesChildTable(resp)
//     });
// };

// const delivery_trip = () => {
//     const event = "delivery_trip";
//     console.log(`##########################->| ${event} |<-###############################`);
//     getRouteCustomersExistingReturnables();
// };


const serial_numbers = () => {
    const event = "serial_numbers";
    console.log(`##########################->| ${event} |<-###############################`);

    const { frm } = this;
    const { doc } = frm;
    const { AllSerialNumbers } = doc;
    const { custody_group, lookup } = AllSerialNumbers;
    const enteredSNs = doc.serial_numbers.replace(/,/g, ' ').replace(/\n+/g, ' ').replace(/\s\s+/g, ' ').replace(/\s+$/g, '').split(' ');
    console.log(`enteredSNs: split into [${enteredSNs}]`);

    const tmp = []
    enteredSNs.forEach(SN => {
        // console.log(`SN : ${SN} => ${lookup[SN]}`);
        if (lookup[SN]) { tmp.push(SN) }
    })

    const valid_sns = tmp.sort();
    doc.valid_sn = valid_sns.join(', ');

    if ( doc.valid_sn !== doc.old_valid_sn ) {
        doc.old_valid_sn = doc.valid_sn;
        frm.clear_table("customer_returnables")
        frm.refresh_fields();
        console.log(` * * * VALID VALUES HAVE CHANGED * * * `);
        console.dir(frm);

        let rowNum = 1;
        const check = [];
        valid_sns.forEach(serial_number => {
            const customer = lookup[serial_number];
            console.log(`sn: ${serial_number},  cust: ${customer}`);
            console.log(`pw: ${lookup[serial_number].parent_warehouse},  cust: ${custody_group}`);

            let chk = false;
            let color = "red";
            if (lookup[serial_number]) {
                if (lookup[serial_number].parent_warehouse === custody_group) {
                    color = "green";
                    chk = true;
                }
            }
            check.push(chk);
            frm.add_child('customer_returnables', {
                "selected": chk,
                "serial_number": serial_number,
                "location": `<p style='color:${color};'>${lookup[serial_number].warehouse}</p>`,
                "consignment": lookup[serial_number].warehouse
            });

            // const row = frm.fields_dict.customer_returnables.grid.grid_rows[rowNum]
            // row.select(true);
            // row.refresh_check();

            rowNum += 1;
        });
        frm.refresh_field('customer_returnables')
        console.dir(frm.fields_dict.customer_returnables.grid.grid_rows);
        console.dir(check);

        for ( let idx = 0; idx < check.length; idx += 1) {
            const row = frm.fields_dict.customer_returnables.grid.grid_rows[idx];
            row.select(check[idx]);
            row.refresh_check();
        }

        // frm.fields_dict.customer_returnables.grid.grid_rows.forEach(row => {
        //     row.select(true);
        //     row.refresh_check();
        // });
    }




    // console.log(quickSearch)
    // console.log(lookup)
    // getRouteCustomersExistingReturnables();
};


const prepare_globals = (event) => {
    console.log(`########################## -->| ${event} |<-- ############################`);
    const { frm } = this;
    const { doc } = frm;

    doc.allSerialNumbers = "";
    doc.old_valid_sn = "";
    const method = "returnable.returnable.doctype.returnables_batch_transfers.returnables_batch_transfers.getAllSerialNumbers";
        frappe.call({ method,
        args: {},
        callback: resp => {
            // const { message: lookup } = resp;
            doc.AllSerialNumbers = resp.message;
            console.log(doc.AllSerialNumbers);
            if (event == "after_save") {
                let idx = 0;
                frm.fields_dict.customer_returnables.grid.grid_rows.forEach(row => {
                    row.select(doc.customer_returnables[idx].selected);
                    row.refresh_check();
                    console.log(`---> ${doc.customer_returnables[idx].selected}`)
                    idx += 1;
                });
            } else {
                serial_numbers();
            }
        }
    });
};

const onload_post_render = () => {
    const event = "onload_post_render";
    prepare_globals(event)
};

const after_save = () => {
    const event = "after_save";
    prepare_globals(event)
};

const before_submit = () => {
    const msg = ` * * * CURTAILED * * * `;
    // frappe.msgprint(__(`${msg}`));
    // frappe.validated = false;
    console.log("*******************>|<*******************");
};

frappe.ui.form.on('Serialized Batch Returns', { serial_numbers, onload_post_render, after_save, before_submit });
