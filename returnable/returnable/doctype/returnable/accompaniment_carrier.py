# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

import frappe
import json

mockResponse = {
    "inserts": [{
      "item_code": "Tapa para botellon 5GL",
      "qty": 88,
      "uom": "Unidad(es)",
      "warehouse": "Embalaje Iridium Blue - LSSA"
    }],
    "updates": [{
      "item_code": "FICHA - para envase IB de 5GL",
      "qty": 7
    }]
}

def collectStockEntryItemAttributes(item):
    item.setdefault("t_warehouse", "")
    item.setdefault("s_warehouse", "")
    return frappe._dict({
        "t_warehouse": item["t_warehouse"],
        "s_warehouse": item["s_warehouse"],
        "qty": item["qty"],
    })
def collectDeliveryNoteItemAttributes(item):
    return frappe._dict({
        "warehouse": item["warehouse"],
        "qty": item["qty"],
    })
collectDeliveryNoteItemAttributes = frappe._dict({
    "Stock Entry": collectStockEntryItemAttributes,
    "DeliveryNote": collectDeliveryNoteItemAttributes,
})

sqlUnionOfRequiringAndRequired = """
    SELECT
        B.item_name,
        B.item_code,
        B.description,
        B.stock_uom,
        B.requires_accompaniment,
        B.required_accompaniment,
        "" AS default_warehouse
    FROM
        tabItem A left join tabItem B
            on B.item_code = A.required_accompaniment
    WHERE
        A.requires_accompaniment > 0
UNION ALL
    SELECT
        B.item_name,
        B.item_code,
        B.description,
        B.stock_uom,
        B.requires_accompaniment,
        B.required_accompaniment,
        D.default_warehouse
    FROM
        `tabItem` B, `tabItem Default` D 
    WHERE
            B.requires_accompaniment > 0
        AND B.item_name = D.parent
    ;
"""
def getAllAccompanimentItems():
    accom = frappe.db.sql(sqlUnionOfRequiringAndRequired, as_dict=1)
    # print(json.dumps(accom, sort_keys=True, indent=4))

    requires = frappe._dict({ })
    required = frappe._dict({ })
    spec = frappe._dict({ })
    accompanimentLookupDicts = frappe._dict({ "required": required, "requires": requires, "spec": spec })
    for idx, item in enumerate(accom):
        code = item.item_code
        accompanimentLookupDicts.spec[code] = item
        if item.requires_accompaniment:
            accompanimentLookupDicts.requires[code] = item.required_accompaniment
        else:
            accompanimentLookupDicts.required[code] = { "requirer": "" }

    for item, value in accompanimentLookupDicts.requires.items():
        # print (json.dumps(value, sort_keys=True, indent=4))
        accompanimentLookupDicts.required[value]["requirer"] = item

    # return accom
    return accompanimentLookupDicts

def collectRequiringActualItems(doc_type, dictChildItems, allAccompanimentItems):
    itemsRequiringAccompanimentSet = set([])
    actualItems = {}

    for item_code in dictChildItems:
        # print(f"DELIVERY NOTE ITEM :: {item_code}")
        if item_code in allAccompanimentItems.requires:
            # print(f"Requirer : {item_code}")
            if item_code not in itemsRequiringAccompanimentSet:
                itemsRequiringAccompanimentSet.add(item_code)
                actualItems[item_code] = collectDeliveryNoteItemAttributes[doc_type](dictChildItems[item_code])
            else:
                actualItems[item_code]["qty"] = actualItems[item_code]["qty"] + dictChildItems[item_code]["qty"]

            requiredCode = allAccompanimentItems.requires[item_code]
            if requiredCode not in itemsRequiringAccompanimentSet:
                itemsRequiringAccompanimentSet.add(requiredCode)
            actualItems[requiredCode] = actualItems[item_code].copy()

    return actualItems

def collectRequiredActualItems(dictChildItems, allAccompanimentItems, requiringActualItems):
    for item_code in dictChildItems:
        # print(f"DELIVERY NOTE ITEM :: {item_code}")
        if item_code in allAccompanimentItems.required:
            # print(f"Required : {item_code}")
            if item_code in requiringActualItems:
                if requiringActualItems[item_code]["qty"] < dictChildItems[item_code]["qty"]:
                    # print(f"Fix : {item_code}")
                    requiringActualItems[item_code]["qty"] = dictChildItems[item_code]["qty"]

    return requiringActualItems

def getCurrentAccompanimentItems(doc_type, dictChildItems, allAccompanimentItems):
    requiringActualItems = collectRequiringActualItems(doc_type, dictChildItems, allAccompanimentItems)
    # print(f"Requiring Actual Items : {json.dumps(requiringActualItems, sort_keys=True, indent=4)}")

    currentAccompanimentItems = collectRequiredActualItems(dictChildItems, allAccompanimentItems, requiringActualItems)
    return currentAccompanimentItems

def getInsertsAndUpdates(dictChildItems, accompanimentItems, allAccompanimentItems):
    insertsAndUpdates = frappe._dict({ "inserts": [], "updates": {} })
    for item in accompanimentItems:
        requiringItem = accompanimentItems[item]
        itemSpec = allAccompanimentItems.spec[item]
        # print(f"""Item :", {item}\n    Content :", {itemSpec}""")

        requiringItem["item_code"] = item
        requiringItem["item_name"] = itemSpec.item_name
        requiringItem["description"] = itemSpec.description
        requiringItem["uom"] = itemSpec.stock_uom
        if item not in dictChildItems:
            print(f"""Insert Item :", {item}        Content :", {requiringItem}""")
            insertsAndUpdates.inserts.append(requiringItem)
        else:
            if item in allAccompanimentItems.required.keys():

                existingQuantity = dictChildItems[item]["qty"]
                print(f"""Update Item :", {item}       Content :", {requiringItem}""")
                print(f"""Existing Quantity : {existingQuantity} New Qty {requiringItem["qty"]} * * * * """)
                if existingQuantity < requiringItem["qty"]:
                    correctQuantity = requiringItem["qty"]
                    requiredItem = accompanimentItems[item]

                insertsAndUpdates.updates[item] = requiringItem

    return insertsAndUpdates

def getConciseDocTypeChildItems(doc_type, DocTypeChildItems):
    conciseChildItems = frappe._dict()
    for childItem in DocTypeChildItems:
        item_code = childItem['item_code']
        if item_code in conciseChildItems:
            conciseChildItems[item_code].qty = conciseChildItems[item_code].qty + childItem["qty"]
        else:
            conciseChildItems[item_code] = collectDeliveryNoteItemAttributes[doc_type](childItem)
    return conciseChildItems

@frappe.whitelist()
def getCarrierAccompanimentItems(doc_type, doc_items):

    insertsAndUpdates = { "inserts": "dummy", "updates": "dummy" }
    # DocTypeChildItems = json.loads(doc_items)
    dictChildItems = getConciseDocTypeChildItems(doc_type, json.loads(doc_items))
    # print("dictChildItems")
    # print (json.dumps(dictChildItems, sort_keys=True, indent=4))

    allAccompanimentItems = getAllAccompanimentItems()
    # print("allAccompanimentItems")
    # print (json.dumps(allAccompanimentItems, sort_keys=True, indent=4))

    accompanimentItems = getCurrentAccompanimentItems(doc_type, dictChildItems, allAccompanimentItems)
    # print("accompanimentItems")
    # print (json.dumps(accompanimentItems, sort_keys=True, indent=4))

    insertsAndUpdates = getInsertsAndUpdates(dictChildItems, accompanimentItems, allAccompanimentItems)
    print("insertsAndUpdates")
    print (json.dumps(insertsAndUpdates, sort_keys=True, indent=4))

    print("%%%%%%%%%%%%%%%% getDeliveryNoteAccompanimentItems %%%%%%%%%%%%%%")
    # return frappe._dict(mockResponse)
#     return accompanimentItems
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~ {doc_type}   ~~~~~~~~~~~~~~~~~~~~~~~~~", flush = True)
    return insertsAndUpdates
