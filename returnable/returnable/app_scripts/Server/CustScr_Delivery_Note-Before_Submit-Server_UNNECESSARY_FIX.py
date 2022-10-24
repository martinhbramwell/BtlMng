# --------------------------------------------------
cmpny = frappe.get_doc("Company", doc.company)
target_warehouse = f"{doc.customer} - {cmpny.abbr}"
if frappe.db.exists('Warehouse', target_warehouse):
    whse = frappe.get_doc('Warehouse', target_warehouse)
    # msg = "Found"
else:
    # frappe.msgprint(
    #     msg=f"Creating warehouse for {doc.customer}",
    #     title='Warn'
    # )
    whse = frappe.get_doc({
        'doctype': 'Warehouse',
        "warehouse_name": doc.customer,
        "parent_warehouse": "Envases IB Custodia del Cliente - LSSA",
        "account": "1.1.5.06 - Envases Custodiados - LSSA",
        "is_group": 0
    }).insert()
    # msg = "New"

# frappe.msgprint( msg = f"Warehouse {target_warehouse}", title = 'Warn' )
# frappe.msgprint( msg = f"Warehouse {whse}", title = 'Warn' )
# raise frappe.ValidationError

msg = []
sep = ""
accompaniers = []
msg.append("Items:: ")

for dnItem in doc.items:
    stItem = frappe.get_doc("Item", dnItem.item_code)
    if stItem.required_accompaniment is not None:
        accompaniers.append(stItem.required_accompaniment)
    msg.append(dnItem.item_code)
    sep = ", "

# msg.append(f" | Requiring accompaniment : {len(accompaniers)}")
# frappe.msgprint( msg = ''.join(msg), title = 'Warn' )
# raise frappe.ValidationError

if len(accompaniers) > 0:
    sep = ""
    row_numbers = []
    idx = 0
    for dnItem in doc.items:
        if dnItem.item_code in accompaniers:
            row_numbers.append(idx)
        idx = idx + 1

    reversed_row_numbers = sorted(row_numbers, reverse=True)
    msg.append(f" --  First unsorted :: {str(row_numbers[0])}, ")
    msg.append(f"List length :: {len(row_numbers)}, ")
    msg.append(f"Reversed List length :: {len(reversed_row_numbers)}, ")
    msg.append(f"First sorted :: {str(reversed_row_numbers[0])}, ")
    # frappe.msgprint( msg = ''.join(msg), title = 'Warn' )

    se = {
            'doctype': 'Stock Entry',
            'docstatus': 0,
            'delivery_note_no:': doc.name,
            'stock_entry_type': 'Material Transfer',
            "items": [] }

    for row in reversed_row_numbers:
        dnItem = doc.items[row]
        msg.append(sep)
        msg.append(dnItem.item_code)
        msg.append(f" ('{dnItem.warehouse}', '{dnItem.serial_no}', '{whse.name}')")
        newRow = {
            't_warehouse': whse.name,
            's_warehouse': dnItem.warehouse,
            'item_code': dnItem.item_code,
            'qty': dnItem.qty,
            'basic_rate': 0.00,
            'additional_cost': 0.00,
            'valuation_rate': 0.00,
            'basic_rate': 0.00,
            'basic_amount': 0.00,
            'amount': 0.00,
            'allow_zero_valuation_rate': 1,
            'serial_no': dnItem.serial_no
        }
        se['items'].append(newRow)
        doc.items.remove(dnItem)
        sep = ", "

    se["from_warehouse"] = dnItem.warehouse;
    se["to_warehouse"] = whse.name;

    # frappe.msgprint( msg = ''.join(msg), title = 'Warn' )

    material_transfer = frappe.get_doc(se).insert()
    material_transfer.save()

    material_transfer.reload()
    material_transfer.docstatus = 1
    material_transfer.save()
    # frappe.msgprint( msg = f"Server Script :: Delivery Note Before Submit ==> {material_transfer.name} , {material_transfer.docstatus}", title = 'Info' )

    # raise frappe.ValidationError
