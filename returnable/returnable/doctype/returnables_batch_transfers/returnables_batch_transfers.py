# Copyright (c) 2022, Warehouseman and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document


stock_entry_start = """{
	"stock_entry_type": "Material Transfer",
	"items": [
"""

stock_entry_end = """{
    ]
}
"""


class ReturnablesBatchTransfers(Document):
	def before_submit(self):
		print(f"""<<<<<<<<<< before submit >>>>>>>>\n{self.direction}""")

		company = frappe.db.get_single_value('Global Defaults', 'default_company')
		defaults = frappe.db.get_value('Company', company, ['envases_sucios', 'envases_llenos'], as_dict=1)
		sqlSucioLlenoLocations = f"""
			SELECT W.name, if(W.account = '{defaults.envases_sucios}', "Cliente >> Sucios", "Sucios >> Llenos") as direction
			  FROM `tabWarehouse` W
			 WHERE W.parent_warehouse = 'Envases Iridium Blue - LSSA'
			   AND W.account IN (
			         '{defaults.envases_llenos}'
			       , '{defaults.envases_sucios}'
			   )
	  """

		dictSucioLlenoLocations = frappe.db.sql(sqlSucioLlenoLocations, as_dict=1)
		directionLookUp = {}
		for location in dictSucioLlenoLocations:
			directionLookUp[location.direction] = location.name

		validTransfers = frappe._dict({})
		report = """"""
		sep = """\n"""
		for rtbl in self.customer_returnables:
			print("returnable... ")
			print(f"   - Selected: {rtbl.selected}\n   - S/N: {rtbl.serial_number}\n   - Location: {rtbl.location}\n   - Consignment: {rtbl.consignment}")
			# print(json.dumps(rtbl, indent=4, default=vars))
			if (rtbl.selected):
				if rtbl.consignment in validTransfers:
					validTransfers[rtbl.consignment].SNs = validTransfers[rtbl.consignment]['SNs'] + "\n" + rtbl.serial_number
				else:
					validTransfers[rtbl.consignment] = frappe._dict({ 'SNs': "", 'count': 0 })
					validTransfers[rtbl.consignment].SNs = rtbl.serial_number

				validTransfers[rtbl.consignment].count += 1

			# rtbl.location = rtbl.consignment

		stock_entry = frappe.get_doc({
		  'doctype': 'Stock Entry',
		  'docstatus': 0,
		  'stock_entry_type': 'Material Transfer'
		})

		items = []
		for source in validTransfers:
			stock_entry.append('items', {
			  's_warehouse': source,
			  't_warehouse': directionLookUp[self.direction],
			  'item_code': "FICHA - para envase IB de 5GL",
			  'serial_no': validTransfers[source].SNs,
			  'qty': validTransfers[source].count
			})
			# stock_entry_item = {
   #      's_warehouse': source,
   #      't_warehouse': directionLookUp[self.direction],
   #      'item_code': "FICHA - para envase IB de 5GL",
   #      'serial_no': validTransfers[source].SNs,
   #      'qty': validTransfers[source].count
			# }
			# items.append(stock_entry_item)
			print(f"Transfer {validTransfers[source]['count']} ({validTransfers[source]['SNs']}) from {source} to {directionLookUp[self.direction]}")

		# stock_entry.append('items', items)
		stock_entry.save()
		stock_entry.submit()

		# # frappe.throw(f"""\n\n\n ### customer_returnables: {stock_entry}\n* * * SERVERSIDE CURTAILED * * * """)
		# frappe.throw(f"""\n\n\n ### customer_returnables: \n* * * SERVERSIDE CURTAILED * * * """)


def orderBySerialNumber(customerSerialNumbers):
  customerOfSerialNumber = []
  for customer in customerSerialNumbers:
    customerName = customer["customer"]
    # print(customerName)
    for serial_number in customer["serial_nos"]:
      # print(serial_number)
      customerOfSerialNumber.append({ "serial_number": serial_number, "customer": customerName })

  customerOfSerialNumber.sort(key=lambda entry: entry["serial_number"])
  return customerOfSerialNumber

def convertToDictionary(customerSerialNumbers):
  customerOfSerialNumber = {}
  for customer in customerSerialNumbers:
    customerName = customer["customer"]
    # print(customerName)
    for serial_number in customer["serial_nos"]:
      # print(serial_number)
      customerOfSerialNumber[serial_number] = customerName
      # customerOfSerialNumber.append({ "serial_number": serial_number, "customer": customerName })

  # customerOfSerialNumber.sort(key=lambda entry: entry["serial_number"])
  return customerOfSerialNumber

def getCustomerReturnables(stop):
	customer = stop.customer
	stock = frappe.db.sql(f'select name from `tabSerial No` where warehouse="{customer} - LSSA"')
	serial_nos = []
	sep = ""
	for serial_no in stock:
		# print(f's/n: {serial_no[0]}')
		serial_nos.append(serial_no[0])
		sep = "\n"

	# print(f's/n: {serial_nos}')
	return { "customer": customer, "serial_nos": serial_nos }

@frappe.whitelist()
def getRouteCustomersExistingReturnables(delivery_trip):
	print("%%%%%%%%%%%%%%%% getRouteCustomersExistingReturnables %%%%%%%%%%%%%%")
	trip = frappe.get_doc('Delivery Trip', delivery_trip)
	# print(type(trip.delivery_stops))
	# print(trip.delivery_stops[0].customer)
	customer_returnables = [ getCustomerReturnables(stop) for stop in trip.delivery_stops ]
	# customerOfSerialNumber = {}
	# for sn in customer_returnables:
	# 	print(json.dumps(sn, indent=4))
	# 	customerOfSerialNumber[sn.serial_number] = sn.customer
	customerOfSerialNumber = convertToDictionary(customer_returnables)
	print(json.dumps(customerOfSerialNumber, indent=4, sort_keys=True))

	return customerOfSerialNumber

sqlStorageLocation = """
	SELECT S.name, S.warehouse, W.parent_warehouse
	FROM `tabSerial No` S LEFT JOIN `tabWarehouse` W 
	ON W.name = S.warehouse
"""

regex = r'[^0-9a-zA-Z\s ]'
sqlConsignmentGroup = f"""
	SELECT W.parent_warehouse
	FROM `tabWarehouse` W 
	WHERE UPPER(REGEXP_REPLACE(REGEXP_REPLACE(concat(W.name), '[[:space:]]', ''), '{regex}', ''))
	IN (
	   SELECT UPPER(REGEXP_REPLACE(REGEXP_REPLACE(concat(C.name, ' - ', C.abbr), '[[:space:]]', ''), '{regex}', ''))
	   FROM `tabCompany` C LEFT JOIN `tabSingles` S ON S.value = C.name 
	   WHERE doctype = "Global Defaults" and field = "default_company"
	);
"""

# select name, abbr from `tabCompany` C left join `tabSingles` S on S.value = C.name where doctype = "Global Defaults" and field = "default_company";

@frappe.whitelist()
def getAllSerialNumbers():
	print("%%%%%%%%%%%%%%%% getAllSerialNumbers %%%%%%%%%%%%%%")

	objSerialNumbers = {};
	arySerial_numbers = frappe.db.sql(sqlStorageLocation, as_dict=0)
	parentLocation = frappe.db.sql(sqlConsignmentGroup, as_dict=0)[0][0]
	print(f"%%%%%% {parentLocation} %%%%%%%%")
	for row in arySerial_numbers:
		# print(f" -- {row[0]} ")
		objSerialNumbers[row[0]] = { "warehouse": row[1], "parent_warehouse": row[2] }

	return { "custody_group": parentLocation, "lookup": objSerialNumbers }
