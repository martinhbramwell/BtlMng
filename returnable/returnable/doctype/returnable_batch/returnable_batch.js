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

const full = alreadyChosen => {
  alreadyChosen.filters.push(["Returnable", "state", "=", "Lleno"]);
  return alreadyChosen;
};

const empty = alreadyChosen => {
  alreadyChosen.filters.push(["Returnable", "state", "=", "Sucio"]);
  return alreadyChosen;
};

const noData = alreadyChosen => {
  alreadyChosen.filters.push(["Returnable", "state", "=", "Find none"]);
  return alreadyChosen;
};

const stocks = {
  'Envases IB Llenos - LSSA': full,
  'Envases IB Sucios - LSSA': empty,
  '': noData,
}

const fromStockLookUp = (alreadyChosen, source) => {
  console.log(`fromStockLookUp :: alreadyChosen`);
  console.dir(alreadyChosen);
  console.dir(source);
  return stocks[source.fromStock](alreadyChosen);
};

const fromCustLookUp = (alreadyChosen, source) => {
  alreadyChosen.filters.push(["Returnable", "last_customer", "=", source.fromCustomer]);
  alreadyChosen.filters.push(["Returnable", "state", "=", "Donde Cliente"]);
  console.log(`fromCustLookUp: `);
  console.dir(alreadyChosen);
  return alreadyChosen;
};

// const setStockCust = alreadyChosen => full(alreadyChosen);
const setStockStock = (alreadyChosen, source) => fromStockLookUp(alreadyChosen, source);
const setFromCust = (alreadyChosen, source) => fromCustLookUp(alreadyChosen, source);

const stateLookUp = {};
stateLookUp[`${custCust}`] = setFromCust;
stateLookUp[`${custStock}`] = setFromCust;
stateLookUp[`${stockCust}`] = setStockStock;
stateLookUp[`${stockStock}`] = setStockStock;

const contentsBottlesMoved = (frm) => {
  const returnables = [];
  const tmp = frm.doc.bottles_moved || [];
  tmp.forEach(row => returnables.push(["Returnable", "name", "!=", row.bottle]));
  return { filters: returnables };
}

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

  const DFS = FS;
  const DFC = "Envases IB Llenos - LSSA";
  const DTS = "Envases IB Sucios - LSSA";
  const DTC = TC;
  const disallowMove = { "from": {}, "to": {} };
  disallowMove.to[custCust] = DFC;
  disallowMove.to[custStock] = DFC;
  disallowMove.to[stockCust] = DFS;
  disallowMove.to[stockStock] = DFS;
  disallowMove.from[custCust] = DTC;
  disallowMove.from[custStock] = DTC;
  disallowMove.from[stockCust] = DTS;
  disallowMove.from[stockStock] = DTC;


  const alreadyChosen = contentsBottlesMoved(frm);
  console.log('alreadyChosen');
  console.dir(alreadyChosen);
  const returnablesFilters = stateLookUp[dir](alreadyChosen, { fromStock: FS, fromCustomer: FC });
  console.log('returnablesFilters...');
  console.dir(returnablesFilters);
  let cnt = 1;
  returnablesFilters.filters.forEach(filter => {
    console.log(` ${cnt}/. Filter : ${filter[0]}'s ${filter[1]} ${filter[2]} '${filter[3]}'`);
  });

  returnablesTable.get_field('bottle').get_query = () => returnablesFilters;

  cur_frm.fields_dict.to_stock.get_query = 
    () => ({ filters: [
      ["Warehouse", "parent", "=", "Envases Iridium Blue - LSSA"],
      ["Warehouse", "name", "!=", disallowMove.to[dir]],
    ] });


  cur_frm.fields_dict.from_stock.get_query = 
    () => ({ filters: [
      ["Warehouse", "parent", "=", "Envases Iridium Blue - LSSA"],
      ["Warehouse", "name", "!=", disallowMove.from[dir]],
      ["Warehouse", "name", "!=", "Envases IB Rotos - LSSA"],
    ] });


  cur_frm.fields_dict.to_customer.get_query = 
    () => ({ filters: [
      ["Customer", "name", "!=", disallowMove.to[dir]],
    ] });

  cur_frm.fields_dict.from_customer.get_query = 
    () => ({ filters: [
      ["Customer", "name", "!=", disallowMove.from[dir]],
    ] });

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
    console.log(`setup ${frm.doc.direction}`);
    adjustForDirection(frm);
    frm.set_value('timestamp', frappe.datetime.now_datetime());
    frm.set_df_property('timestamp', 'read_only', 1);
  },
  onload: function(frm) {
    console.log('onload');
    adjustForDirection(frm);
  },
  refresh: async function(frm) {
    console.log(`refreshed : ${frm.doc.direction}`);
  },
  validate: (frm, cdt, cdn) => {
    console.log(`Validating '${cdt}' :: ${cdn}`);
  },
  direction: (frm, cdt, cdn) => {
    console.log(`Direction :: ${frm.doc.direction}`);
    adjustForDirection(frm);
    frm.clear_table("bottles_moved")
    frm.refresh_field('bottles_moved');
    frm.refresh();
  },
  from_customer: (frm, cdt, cdn) => {
    console.log(`From Customer '${frm.doc.from_customer}' to  TS: '${frm.doc.to_stock}' TC: '${frm.doc.to_customer}'`);
    frm.clear_table("bottles_moved")
    frm.refresh_field('bottles_moved');
    adjustForDirection(frm);
    frm.refresh();
  },
  from_stock: (frm, cdt, cdn) => {
    console.log(`From Stock '${frm.doc.from_stock}' to  TS: '${frm.doc.to_stock}' TC: '${frm.doc.to_customer}'`);
    frm.clear_table("bottles_moved")
    frm.refresh_field('bottles_moved');
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
  specify_date: (frm, cdt, cdn) => {
    console.log(`specify_date ${cdn} (${cdt}):  ${frm.doc.specify_date}` );
    console.dir(frappe.datetime);
    frm.set_df_property('timestamp', 'read_only', ! frm.doc.specify_date)
    frm.set_value('timestamp', frappe.datetime.now_datetime());
  }
});

frappe.ui.form.on('Returnable Batch Item', {
  bottle: (frm, cdt, cdn) => {
    console.log(`ON Returnable Batch Item >> bottle ${cdn} (${cdt}):`);
    adjustForDirection(frm);
  },

  form_render: (frm, cdt, cdn) => {
    console.log(`Returnable Batch Item: form_render`);
  },
});
