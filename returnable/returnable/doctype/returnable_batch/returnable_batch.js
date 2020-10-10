const returnablesBatch = cur_frm.fields_dict;
const returnablesTable = returnablesBatch.bottles_moved.grid;


const toCust = '> Cust';
const toStock = '> Stock';
const fromCust = 'Cust >';
const fromStock = 'Stock >';

const custCust = `${fromCust}${toCust}`;
const custStock = `${fromCust}${toStock}`;
const stockCust = `${fromStock}${toCust}`;
const stockStock = `${fromStock}${toStock}`;

const full = { filters: [["Returnable", "state", "=", "Lleno"]] };
const empty = { filters: [["Returnable", "state", "=", "Vacio"]] };
// const broken = { filters: [["Returnable", "state", "=", "Lleno"]] };
const atClient = { filters: [["Returnable", "state", "=", "Donde Cliente"]] };
;
const notAtClient = { filters: [["Returnable", "state", "!=", "Donde Cliente"]] };

const fromStockLookUp = {
  'Envases IB Llenos - LSSA': full,
  'Envases IB Sucios - LSSA': empty,
  '': notAtClient,
};
  // 'Envases IB Rotos - LSSA': broken,


const fromCustLookUp = (source) => {
  const fil = { filters: [["Returnable", "state", "=", "Donde Cliente"], ["Returnable", "last_customer", "=", source]] };
  console.dir(fil);
  return fil;
};

// const setFromCust = () => empty;
const setStockCust = () => full;

const setStockStock = (stock = '', customer = '') => fromStockLookUp[stock];
// const setStockStock = (stock = '', customer = '') => () => {
//   console.log('!!!!!!!!');
//   return 'qwerty';
// };

// const setCustCust = (stock = '', customer = '') => fromCustLookUp(customer);
const setFromCust = (stock = '', customer = '') => fromCustLookUp(customer);

const stateLookUp = {};
// stateLookUp['Cust >> Cust'] = setFromCust;
// stateLookUp['Cust >> Stock'] = setFromCust;
// stateLookUp['Stock >> Cust'] = setStockCust;
// stateLookUp['Stock >> Stock'] = setStockStock;
stateLookUp[`${custCust}`] = setFromCust;
stateLookUp[`${custStock}`] = setFromCust;
stateLookUp[`${stockCust}`] = setStockCust;
stateLookUp[`${stockStock}`] = setStockStock;

function adjustForDirection(frm) {
  const dir = frm.doc.direction;
  const TS = frm.doc.to_stock || '';
  const TC = frm.doc.to_customer || '';
  const FS = frm.doc.from_stock || '';
  const FC = frm.doc.from_customer || '';

  console.log(`Function adjustForDirection (${dir}) 
    FS: >${FS}< 
    FC: >${FC}< 
    TS: >${TS}< 
    TC: >${TC}<
  `);

  const fil = stateLookUp[dir](FS, FC);
  console.log('fil...');
  console.dir(fil);
  returnablesTable.get_field('bottle').get_query = () => fil;

  cur_frm.fields_dict.to_stock.get_query = 
    () => ({ filters: [
      ["Warehouse", "parent", "=", "Envases Iridium Blue - LSSA"],
      ["Warehouse", "name", "!=", FS],
    ] });

  cur_frm.fields_dict.from_stock.get_query = 
    () => ({ filters: [
      ["Warehouse", "parent", "=", "Envases Iridium Blue - LSSA"],
      ["Warehouse", "name", "!=", TS],
      ["Warehouse", "name", "!=", "Envases IB Rotos - LSSA"],
    ] });


  cur_frm.fields_dict.to_customer.get_query = 
    () => ({ filters: [
      ["Customer", "name", "!=", FC],
    ] });

  cur_frm.fields_dict.from_customer.get_query = 
    () => ({ filters: [
      ["Customer", "name", "!=", TC],
    ] });

  // cur_frm.get_field('to_stock').get_query = () => { filters: [["Warehouse", "parent", "=", "Envases Iridium Blue - LSSA"]] };
  // cur_frm.get_field('from_stock').get_query = () => { filters: [["Warehouse", "parent", "=", "Envases Iridium Blue - LSSA"]] };

  // returnablesTable.refresh_field('bottle');
  frm.refresh_field('bottles_moved');

  frm.set_df_property('to_customer', 'reqd', dir.includes(toCust));
  frm.set_df_property('from_customer', 'reqd', dir.includes(fromCust));
  frm.set_df_property('to_stock', 'reqd', dir.includes(toStock));
  frm.set_df_property('from_stock', 'reqd', dir.includes(fromStock));

  frm.set_df_property('to_customer', 'hidden', dir.includes(toStock));
  frm.set_df_property('from_customer', 'hidden', dir.includes(fromStock));
  frm.set_df_property('to_stock', 'hidden', dir.includes(toCust));
  frm.set_df_property('from_stock', 'hidden', dir.includes(fromCust));

}

frappe.ui.form.on('Returnable Batch', {
	setup: function(frm) {
    console.log(`setup ${frm.doc.direction} >${returnablesTable}<`);
    console.dir(returnablesTable);
    adjustForDirection(frm);
    frm.set_value('timestamp', frappe.datetime.now_datetime());
    frm.set_df_property('timestamp', 'hidden', 0);
    // frm.set_value('timestamp', Date.now());
  },
  onload: function(frm) {
    console.log('onload');
    adjustForDirection(frm);
  },
  refresh: async function(frm) {
    console.log(`refreshed : ${frm.doc.direction}`);
    // const resp = await cur_frm.call({
    //   method: "loadReturnablesStates",
    //   args: { direction: frm.doc.direction }
    // });
    // console.log(resp.message);
  },
  validate: (frm, cdt, cdn) => {
    console.log(`Validating '${cdt}' :: ${cdn}`);
  },
  direction: (frm, cdt, cdn) => {
    console.log(`Direction :: ${frm.doc.direction}`);
    adjustForDirection(frm);
    
    frm.refresh();
  },
  from_customer: (frm, cdt, cdn) => {
    console.log(`From Customer '${frm.doc.from_customer}' to  TS: '${frm.doc.to_stock}' TC: '${frm.doc.to_customer}'`);
    adjustForDirection(frm);
    frm.refresh();
  },
  from_stock: (frm, cdt, cdn) => {
    console.log(`From Stock '${frm.doc.from_stock}' to  TS: '${frm.doc.to_stock}' TC: '${frm.doc.to_customer}'`);
    adjustForDirection(frm);    
    frm.refresh();
  },
  to_customer: (frm, cdt, cdn) => {
    console.log(`To Customer '${frm.doc.to_customer}' to  FS: '${frm.doc.from_stock}' FC: '${frm.doc.from_customer}'`);
    adjustForDirection(frm);
    frm.refresh();
  },
  to_stock: (frm, cdt, cdn) => {
    console.log(`To Stock '${frm.doc.to_stock}' to  FS: '${frm.doc.from_stock}' FC: '${frm.doc.from_customer}'`);
    adjustForDirection(frm);    
    frm.refresh();
  },
  // to_stock: (frm, cdt, cdn) => {
  //   // const fldFromStock = returnablesBatch.get_field('from_stock');
  //   console.log(`To Stock '${frm.doc.to_stock}' from '${frm.doc.from_stock}'`);
  //   // console.dir(fldFromStock);
  //   adjustForDirection(frm);
  //   // if (frm.doc.direction = stockStock) {
  //   //   returnablesBatch.get_field('from_stock').get_query = 
  //   //     () => ({ filters: [["Warehouse", "name", "=", "Lleno"]] });
  //   // }
  // },
  specify_date: (frm, cdt, cdn) => {
    console.log(`specify_date ${cdn} (${cdt}):  ${frm.doc.specify_date}` );
    console.dir(frappe.datetime);
    frm.set_df_property('timestamp', 'read_only', ! frm.doc.specify_date)
    frm.set_value('timestamp', frappe.datetime.now_datetime());
  }
});

frappe.ui.form.on('Returnable Batch Item', {
  bottle: (frm, cdt, cdn) => {
    console.log(`Returnable Batch Item:`);
    console.log(`    | bottle ${cdn} (${cdt}):`);
  },
  form_render: (frm, cdt, cdn) => {
    console.log(`Returnable Batch Item: form_render`);
  },
});
