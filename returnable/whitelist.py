import frappe

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_returnable_movements(doctype, txt, searchfield, start, page_len, filters):
    query = """
        select
              name
            , creation
            , modified
            , modified_by
            , owner
            , docstatus
            , parent
            , parentfield
            , parenttype
            , idx
            , direction
            , from_stock
            , from_customer
            , to_customer
            , to_stock
            , timestamp
            , bapu_id
            , if_customer
            , transferred
        from `tabReturnable Movement`
        where parent = "{txt}"
        order by idx desc
    """.format (
        txt = frappe.db.escape("%{0}%".format(txt))
    )

    return frappe.db.sql(query)


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
