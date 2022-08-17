import frappe

@frappe.whitelist()
def changeStockEntryType(name, newType):
    print(f"""%%%%%%%%%%%%%%%%%%%%% | {name} | {newType} | %%%%%%%%%%%%%%%%%%%%%%%%%%""")

    dmlChangeStockEntryType = f"""
        UPDATE
            `tabStock Entry`
        SET 
              purpose = '{newType}'
            , stock_entry_type = '{newType}'
        WHERE
            name = '{name}';
    """
    result = frappe.db.sql(dmlChangeStockEntryType, as_dict=1)

    print('updated')
    frappe.db.commit()
    print('committed')
    
    return result
