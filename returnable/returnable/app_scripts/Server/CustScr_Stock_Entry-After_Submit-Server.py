
crlf = ""
msg = ""

msg = f"""{msg}{crlf} -------------------------------"""
crlf = "<br>"

def getFlaggedWarehouses():
    sqlFlaggedWarehouses = """
        SELECT
            json_value(pin, '$.proposito') as proposito,
            name as warehouse
        FROM
            tabWarehouse
        WHERE
            pin IS NOT NULL
        ;
    """
    result = { }
    for flag in frappe.db.sql(sqlFlaggedWarehouses, as_dict=1):
        result[flag.proposito] = flag.warehouse
    return result

listWarehouses = getFlaggedWarehouses()

def getAccompaniments():
    sqlAccompaniments = """
        SELECT distinct
            required_accompaniment
        FROM
            `tabItem`
        WHERE
            required_accompaniment IS NOT NULL
        ;
    """

    result = []
    for item in frappe.db.sql(sqlAccompaniments, as_dict=1):
        result.append(item.required_accompaniment)
    return result

listAccompaniments = getAccompaniments()

CLEAN_ROOM = "cuarto limpio";
DIRTY_BOTTLES = "envases sucios";
FILLED_BOTTLES = "envases llenos";

# def changeStockEntryType(se):
#     dmlChangeStockEntryType = f"""
#         UPDATE
#             `tabStock Entry`
#         SET 
#               purpose = 'Manufacture'
#             , stock_entry_type = 'Manufacture'
#         WHERE
#             name = '{se}';
#     """
#     result = frappe.db.sql(dmlChangeStockEntryType, as_dict=1)
#     frappe.db.commit()
#     return result

# Material Transfer
# Material Transfer
# Envases IB Sucios - LSSA
# Envases IB Llenos - LSSA
# FICHA - para envase IB de 5GL
# Cuarto Limpio - LSSA
# FICHA - para envase IB de 5GL

# accum = 0
accum = 12
accum = (accum | (doc.purpose == "Material Transfer")) << 1
accum = (accum | (doc.items[0].s_warehouse == listWarehouses[DIRTY_BOTTLES])) << 1
accum = (accum | (doc.items[0].t_warehouse == listWarehouses[FILLED_BOTTLES])) << 1
accum = (accum | (doc.items[0].item_code in listAccompaniments)) << 1

msg = f"""{msg}{crlf} accum : {accum:b} ( {accum})"""

if accum == 222:
    # msg = f"""{msg}{crlf} {doc.purpose}"""
    # msg = f"""{msg}{crlf} {doc.stock_entry_type}"""
    # msg = f"""{msg}{crlf} {doc.items[0].t_warehouse}"""
    # msg = f"""{msg}{crlf} {doc.items[0].item_code}"""
    # msg = f"""{msg}{crlf} {listWarehouses['cuarto limpio']}"""
    # msg = f"""{msg}{crlf} {listAccompaniments[0]}"""
    
    msg = f"""{msg}{crlf} Interesting"""
    msg = f"""{msg}{crlf} work_order : >{doc.work_order}<"""
    msg = f"""{msg}{crlf} name : >{doc.name}<"""

    # dmlRslt = changeStockEntryType(doc.name)
    dmlRslt = frappe.call("returnable.whitelist.changeStockEntryType", name = doc.name, newType = 'Manufacture')

    msg = f"""{msg}{crlf} dmlRslt: >{dmlRslt}<"""
    # raise Exception(msg)
    # doc.purpose = "Manufacture"
    # doc.stock_entry_type = doc.purpose
    # doc.save()

else:
    msg = f"""{msg}{crlf} Not Interesting"""
    msg = f"""{msg}{crlf} Type : {doc.purpose} = Material Transfer"""
    msg = f"""{msg}{crlf} Source Whse : {doc.items[0].s_warehouse} = {listWarehouses[DIRTY_BOTTLES]}"""
    msg = f"""{msg}{crlf} Dest Whse : {doc.items[0].t_warehouse} = {listWarehouses[FILLED_BOTTLES]}"""
    msg = f"""{msg}{crlf} Product : {doc.items[0].item_code} is in {listAccompaniments}"""


msg = f"""{msg}{crlf} -------------------------------"""
frappe.msgprint( msg = msg, title = 'Debug' )
