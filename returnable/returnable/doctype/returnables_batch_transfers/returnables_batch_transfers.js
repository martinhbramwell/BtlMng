// Copyright (c) 2022, Warehouseman and contributors
// For license information, please see license.txt


// const emptyStore = {
//     "AllSerialNumbers" : {
//         "custody_group": "Envases IB Custodia del Cliente - LSSA"
//     },
//     "route_consignment_locations": "None"
// };

// const unStore = () => {
//     const method = "unStore";
//     console.log(`########################## -->| ${method}: ${this.frm.docname} |<-- ############################`);
//     return;

//     let LS = null;
//     if (localStorage[this.frm.docname]) {
//         LS = JSON.parse(localStorage[this.frm.docname]);
//     } else {
//         LS = emptyStore;
//     }
//     this.frm.route_consignment_locations = LS.route_consignment_locations;
//     this.frm.AllSerialNumbers = LS.AllSerialNumbers;
// }

// const store = () => {
//     const method = "store";
//     console.log(`########################## -->| ${method}: ${this.frm.docname} |<-- ############################`);
//     return;

//     console.log('this.frm.route_consignment_locations');
//     console.dir(this.frm.route_consignment_locations);
//     localStorage.setItem(
//         this.frm.docname,
//         JSON.stringify({
//             "AllSerialNumbers" : this.frm.AllSerialNumbers,
//             "route_consignment_locations": this.frm.route_consignment_locations
//         }, null, 2)
//     );
// }

const after_save = () => {
    const event = "after_save";
    console.log(`########################## -->| ${event} |<-- ############################`);
    // serial_numbers(event)
    // this.frm.events.repaintcntr(event);
    return;

    // let old_name = localStorage["oldDocName"];
    // const LS = JSON.parse(localStorage[old_name]);
    // // delete localStorage[old_name];

    // localStorage.setItem(this.frm.docname, JSON.stringify(LS, null, 2));
    // localStorage.setItem("oldDocName", this.frm.docname);
    // console.log('this.frm.route_consignment_locations');
    // console.dir(this.frm.route_consignment_locations);

    // console.log(`  ||| TEST: ${this.frm.testicle}`);
    // prepare_globals(event);
};

const before_save = () => {
    const event = "before_save";
    console.log(`########################## -->| ${event} |<-- ############################ ${this.frm.docname}`);

    const { frm } = this;
    const { doc, is_wrong, is_anomaly } = frm;
    const { direction, docstatus } = doc;

    console.log("prepare_globals: frm.is_wrong")
    console.dir(frm.is_wrong)

    for ( let idx = 0; idx < frm.is_wrong.length; idx += 1) {
        console.dir(doc.customer_returnables[idx]);
        let { consignment, location } = doc.customer_returnables[idx];
        console.log(`(BS) ******** consignment: ${consignment},  location: ${location}`);
        const row = frm.fields_dict.customer_returnables.grid.grid_rows[idx];

        const isAnomaly = direction === 'Cliente >> Sucios'  ?  is_anomaly[idx]  :  false;
        const isWrong = is_wrong[idx];

        let color = (isWrong  ?  'red'  : isAnomaly  ?  'orange'  :  'green')
        let selected =  (isWrong || isAnomaly);
        console.log(`idx : ${idx}, color ${color}, selected ${selected} (Anomaly? : ${isAnomaly})`);

        doc.customer_returnables[idx].location = `<p style='color:${color};'>${consignment}</p>`
        doc.customer_returnables[idx].selected = selected;

        this.frm.fields_dict.customer_returnables.grid.grid_rows[idx].select(selected);
        this.frm.fields_dict.customer_returnables.grid.grid_rows[idx].refresh_check();
    }


    return;
};

const before_submit = () => {
    const method = "before_submit";
    console.log(`########################## -->| ${method} |<-- ############################`);

    this.frm.route_consignment_locations = "";

    const { frm } = this;
    const { doc } = frm;
    console.dir(doc);
    // const { customer_returnables } = doc;

    // for (let idx = 0; idx < customer_returnables.length; idx += 1) {
    //     console.log("*******************> | <*******************");
    //     console.dir(customer_returnables[idx]);
    //     console.log("*******************> | <*******************");
    //     let location = customer_returnables[idx].location;
    //     console.dir(location);
    //     console.dir(location.split("'"));
    //     console.dir(location.split("'")[1]);
    //     console.dir(location.split("'")[1].split(":"));
    //     console.dir(location.split("'")[1].split(":")[1]);
    //     console.dir(location.split("'")[1].split(":")[1].replace(';', '|'));
    //     frm.doc.customer_returnables[idx].location =
    //             location.split("'")[1].split(":")[1].replace(';', '|') +
    //             frm.doc.customer_returnables[idx].consignment
    //     console.log("cr");
    //     console.dir(frm.doc.customer_returnables[idx]);
    // }

    // const msg = ` * * * CURTAILED * * * `;
    // console.log("*******************> | <*******************");
    // frappe.msgprint(__(`${msg}`));
    // frappe.validated = false;
};

const fillCustomerReturnablesChildTable = (event) => {
    const method = "fillCustomerReturnablesChildTable";
    console.log(`##########################->| ${method} |<-###############################`);

    // unStore();
    const { frm } = this;
    const { doc } = frm;
    let { route_consignment_locations } = frm;
    let { customer_returnables } = doc;

    console.log(`fillCustomerReturnablesChildTable ==> Context: `);
    console.dir(route_consignment_locations);
    console.log(`----`);
    console.dir(customer_returnables);

    if (customer_returnables && route_consignment_locations && route_consignment_locations != "None") {
        frm.is_anomaly = [];
        let anomalies = ``;
        let sep = ``;

        customer_returnables.forEach(row => {
            const { serial_number, consignment } = row;

            let anomaly = false;
            if (  !  route_consignment_locations[serial_number]) {
                anomalies += `${sep}${consignment}: ${serial_number}`;
                anomaly = true;
                sep = `\n`;
            }

            console.log(`Anomaly: ${anomaly},  cust: ${consignment}`);
            frm.is_anomaly.push(anomaly);
        });

        doc.anomalies = anomalies;

        frm.refresh_field('customer_returnables')
        frm.refresh_field('route_consignment_locations')

    } else {
        doc.anomalies = "";
    }
    frm.refresh_field('anomalies')
    if ( event !== 'prepare_globals' ) frm.events.repaintcntr();
}

const getRouteCustomersExistingReturnables = (event) => {
    const method = "getRouteCustomersExistingReturnables";
    console.log(`##########################->| ${method} |<-###############################`);
    const { frm } = this;
    const { doc } = frm;
    let { delivery_trip } = doc;

    if (delivery_trip) {
        console.log("Calling server >>>>>>>>>>>>>>");
        const method = "returnable.returnable.doctype.returnables_batch_transfers.returnables_batch_transfers.getRouteCustomersExistingReturnables";
    		frappe.call({ method,
            args: { delivery_trip },
            callback: resp => {
                frm.route_consignment_locations = resp.message;

                console.log(`<<<  route_consignment_locations >>>`)
                console.dir(frm.route_consignment_locations);

                // store();
                // TESTIT fillCustomerReturnablesChildTable(event)
            }
        });
    } else {
        console.log("NO Delivery Trip: clearing store >>>>>>>>>>>>>>");
        doc.anomalies = "";
        frm.refresh_field('anomalies')
        for ( let idx = 0; idx < frm.is_anomaly.length; idx += 1) {
            frm.is_anomaly[idx] = false;
        }
        frm.refresh_field('anomalies');
        frm.route_consignment_locations = "None";

        // store();
        // TESTIT fillCustomerReturnablesChildTable(event);
    }
};

const rePaintChildTable = (event) => {
    console.log(`******** docstatus: ${this.frm.doc.docstatus}`);
    const method = "rePaintChildTable";
    console.log(`########################## -->| ${method}: ${event} |<-- ############################`);
    if (event === "after_save") {
        this.frm.doc.serial_numbers += ",";
    }

    const { frm } = this;
    const { doc, is_wrong, is_anomaly } = frm;
    const { direction, docstatus } = doc;

    this.frm.refresh_field('serial_numbers');
    console.log(this.frm.doc.serial_numbers);
    for ( let idx = 0; idx < frm.is_wrong.length; idx += 1) {
        let { consignment, location } = doc.customer_returnables[idx];
        console.log(`(RPC) ******** consignment: ${consignment},  location: ${location}`);
        const row = frm.fields_dict.customer_returnables.grid.grid_rows[idx];

        const isAnomaly = direction === 'Cliente >> Sucios'  ?  is_anomaly[idx]  :  false;
        const isWrong = is_wrong[idx];

        let color = (isWrong  ?  'red'  : isAnomaly  ?  'orange'  :  'green')
        let selected =  (isWrong || isAnomaly);
        console.log(`idx : ${idx}, color ${color}, selected ${selected} (Anomaly? : ${isAnomaly})`);

        doc.customer_returnables[idx].location = `<p style='color:${color};'>${consignment}</p>`
        doc.customer_returnables[idx].selected = selected;

        this.frm.fields_dict.customer_returnables.grid.grid_rows[idx].select(selected);
        this.frm.fields_dict.customer_returnables.grid.grid_rows[idx].refresh_check();
    }
    console.dir(this.frm);
    this.frm.refresh_field('customer_returnables');
    this.frm.refresh();
};

const delivery_trip = () => {
    const event = "delivery_trip";
    console.log(`##########################->| ${event} |<-###############################`);
    getRouteCustomersExistingReturnables(event);
};

const extractValidSerialNumbers = (serial_numbers, lookup) => {
    const enteredSNs = new Set(serial_numbers.replace(/,/g, ' ').replace(/\n+/g, ' ').replace(/\s\s+/g, ' ').replace(/\s+$/g, '').split(' '));

    const valids = []
    enteredSNs.forEach(SN => { if (lookup[SN]) { valids.push(SN) } })

    return valids.sort();
};

const getReturnableDisplaySettings = ctx => {
    const { serial_number, lookup, custody_group } = ctx;
    const { docstatus, customer_returnables, direction } = this.frm.doc;

    // console.log(`sn: ${serial_number},  cust: ${lookup[serial_number].warehouse}`);
    // console.log(`pw: ${lookup[serial_number].parent_warehouse},  cust: ${custody_group}`);

    let wrong = true;
    let color = "red";
    let displayLocation = lookup[serial_number].warehouse;
    if (docstatus === 1) {
        console.log(`customer_returnables[${rowNum - 1}]`);
        console.dir(customer_returnables[rowNum - 1]);
        displayLocation = customer_returnables[rowNum - 1].consignment;
        color = customer_returnables[rowNum - 1].location.split['|'][0];
        wrong = customer_returnables[rowNum - 1].selected;
    } else {
        if (lookup[serial_number]) {
            // console.log(`Direction: ${direction}`);
            if (direction === "Sucios >> Llenos") {
                if (displayLocation === 'Envases IB Sucios - LSSA') {
                    color = "green";
                    wrong = false;
                }
            } else {
                if (lookup[serial_number].parent_warehouse === custody_group) {
                    color = "green";
                    wrong = false;
                }
            }
        }
    }

    // const rowSettings = {
    return {
        "selected": wrong,
        "serial_number": serial_number,
        "location": `<p style='color:${color};'>${displayLocation}</p>`,
        "consignment": displayLocation
    }
};

const serial_numbers = () => {

    const method = "serial_numbers";
    console.log(`##########################->| ${method} |<-###############################`);

    const { frm } = this;
    const { doc } = frm;

    const { serial_numbers, direction, customer_returnables } = doc;

    let { AllSerialNumbers } = frm;
    const { custody_group, lookup } = AllSerialNumbers;

    frm.is_anomaly = [];
    frm.is_wrong = [];

    frm.clear_table("customer_returnables")
    frm.refresh_fields();

    const limit = 50;

    if (serial_numbers && serial_numbers.length > 4) {
        const valid_sns = extractValidSerialNumbers(serial_numbers, lookup);
        if (valid_sns.length > limit) {
            const diff = valid_sns.length - limit;
            const rmv = diff > 1 ? `${diff} deben ser eliminados` : "1 debe ser eliminado";
            const msg = `Se ha superado el límite de ${limit} artículos. ${rmv}.`;
            frappe.msgprint(__(`${msg}`));
            frappe.validated = false;
        } else {
            console.log(`valid_sns : ${valid_sns.length}`)

            doc.valid_sn = valid_sns.join(', ');

            let rowNum = 1;
            valid_sns.forEach(serial_number => {
                const rowSettings = getReturnableDisplaySettings({ serial_number, lookup, custody_group })
                console.log("rowSettings")
                console.dir(rowSettings)

                frm.is_wrong.push(rowSettings["selected"]);
                frm.add_child('customer_returnables', rowSettings);

                rowNum += 1;
            });

            console.log('-------------------');
            // return;
            frm.refresh_field('customer_returnables')
            frm.refresh_fields();
            if ( event !== 'prepare_globals' ) frm.events.repaintcntr();
        }
    }

    // TESTIT fillCustomerReturnablesChildTable('prepare_globals');

};

const prepare_globals = (event) => {
    console.log(`########################## -->| prepare_globals |<-- ############################`);
    // unStore();

    const { frm } = this;
    const { doc } = frm;
    let { AllSerialNumbers, route_consignment_locations } = frm;

    console.log(`  $$$ TEST: ${frm.testicle}`);

    console.log("route_consignment_locations")
    console.dir(route_consignment_locations)

    console.log("AllSerialNumbers")
    console.dir(AllSerialNumbers)

    frm.testicle = "ball";

    if (  ! frm.is_anomaly ) {
        frm.is_anomaly = [];
    }
    console.log("prepare_globals: frm.is_anomaly")
    console.dir(frm.is_anomaly)

    if (  ! frm.is_wrong ) {
        frm.is_wrong = [];
    }
    console.log("prepare_globals: frm.is_wrong")
    console.dir(frm.is_wrong)

    frm.AllSerialNumbers = "";
    doc.old_valid_sn = "";

    // console.dir(doc.customer_returnables[0])
    // return;

    const method = "returnable.returnable.doctype.returnables_batch_transfers.returnables_batch_transfers.getAllSerialNumbers";
        frappe.call({ method,
        args: {},
        callback: resp => {
            frm.AllSerialNumbers = resp.message;
            // localStorage.setItem("AllSerialNumbers", AllSerialNumbers);
            // console.dir(this)
            // console.log("frm.AllSerialNumbers");
            // console.dir(frm.AllSerialNumbers);

            console.log("route_consignment_locations")
            console.dir(route_consignment_locations)
            // store();

            serial_numbers(event);

            // TESTIT fillCustomerReturnablesChildTable(event)

            frm.events.repaintcntr();

        }
    });
};

const onload = () => {
    const event = "onload";
    console.log(`########################## -->| ${event} |<-- ############################ ${this.frm.docname} -->|`);
    // console.dir(this);
};

const onload_post_render = () => {
    const event = "onload_post_render";
    console.log(`########################## -->| ${event} |<-- ############################ ${this.frm.docname} -->|`);
    // this.frm.doc.addEventListener(REPAINT, paintEventListener);
    // console.dir(this);

    prepare_globals(event);
};

const setup = () => {
    const event = "setup";
    console.log(`########################## -->| ${event} |<-- ############################ ${this.frm.docname}`);
    // localStorage.setItem(this.frm.docname, JSON.stringify(emptyStore, null, 2));
    // console.dir(this);
};

const direction = () => {
    const event = "direction";
    console.log(`########################## -->| ${event} |<-- ############################ ${this.frm.docname}`);
    serial_numbers(event)
};

const repaintcntr = (event) => {
    const method = "repaintcntr";
    console.log(`########################## -->| ${method}: ${event} |<-- ############################`);
    rePaintChildTable(event)
};

frappe.ui.form.on('Returnables Batch Transfers', {
    setup,
    onload,
    onload_post_render,
    serial_numbers,
    direction,
    before_save,
    after_save,
    delivery_trip,
    before_submit,
    repaintcntr
});

const removeUnwantedSerialNumbers = () => {
    console.log("called :: removeUnwantedSerialNumbers");
    const { frm } = this;
    const { doc } = frm;

    console.dir(doc.serial_numbers);

    let sep = "";
    let numbers = "";
    for (const returnable of doc.customer_returnables) {
        numbers += sep + returnable.serial_number;
        sep = ", ";
    }
    console.dir(numbers);
    doc.serial_numbers = numbers;
    doc.valid_sn = numbers;
    frm.refresh_field('serial_numbers')
    frm.refresh_field('valid_sn')

    serial_numbers('deleted rows')
};


const TICK_RESOLUTION = 500; // in ms
const TIMER_LENGTH = 1;      // multiples of TICK_RESOLUTION
let endTime = 0;
let timeHdl = 0;
class shortDelay {
    constructor(name, level) {
        endTime = 0;
        timeHdl = 0;
        this.tick = this.tick.bind(this);
    }

    startStopTimer(delay) {
        endTime = performance.now() + Number(delay);        
        this.tick();
        return `Started... ${delay}`
    };

    tick() {
        clearTimeout(timeHdl);
        var till = endTime - performance.now();
        till = till <= 0 ? 0 : till;                
        if (till) {
            timeHdl = setTimeout(this.tick, (till % TICK_RESOLUTION) + 10);
            // console.log("tick");
        } else {
            console.log(" ... we're done!");
            frappe.confirm(
                '¿Está seguro de que desea que esos números de serie se eliminen de la lista que escribió?',
                () => removeUnwantedSerialNumbers(),
                () => frappe.show_alert('Se ha decidido dejar los números de serie como están.!')
            )

        }
    };
};

const aDelay = new shortDelay();

const customer_returnables_remove = (frm, cdt, cdn) => {
    const method = "customer_returnables_remove";
    // console.log(`########################## -->| ${method} |<-- ############################`);
    frm.refresh_field('customer_returnables')
    aDelay.startStopTimer(TIMER_LENGTH * TICK_RESOLUTION);
};

frappe.ui.form.on('Consigned Returnable', {
    customer_returnables_remove
});

/*
           IBCC745, IBCC996, IBCC479, 

IBAA643       IBAA614

IBAA00678       IBAA556
*/
