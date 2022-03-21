# Copyright (c) 2022, Warehouseman and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document

class SerializedBatchReturns(Document):
	def before_submit(self):
		report = """"""
		sep = """\n"""
		for rtbl in self.customer_returnables:
			report += f"""{sep}{rtbl.serial_number} : {rtbl.consignment} : {rtbl.selected}"""

		frappe.throw(f"""\n\n\n ### customer_returnables: {report}\n* * * SERVERSIDE CURTAILED * * * """)


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
	customerOfSerialNumber = orderBySerialNumber(customer_returnables)
	# print(json.dumps(customerOfSerialNumber, indent=4, sort_keys=True))

	return customerOfSerialNumber

sqlStorageLocation = """
	SELECT S.name, S.warehouse, W.parent_warehouse
	FROM `tabSerial No` S LEFT JOIN `tabWarehouse` W 
	ON W.name = S.warehouse
"""

sqlConsignmentGroup = """
	SELECT W.parent_warehouse
	FROM `tabWarehouse` W 
	WHERE UPPER(REGEXP_REPLACE(REGEXP_REPLACE(concat(W.name), '[[:space:]]', ''), '[^0-9a-zA-Z\s ]', ''))
	IN (
	   SELECT UPPER(REGEXP_REPLACE(REGEXP_REPLACE(concat(C.name, ' - ', C.abbr), '[[:space:]]', ''), '[^0-9a-zA-Z\s ]', ''))
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
	for row in arySerial_numbers:
		# print(f" -- {row[0]} ")
		objSerialNumbers[row[0]] = { "warehouse": row[1], "parent_warehouse": row[2] }

	return { "custody_group": parentLocation, "lookup": objSerialNumbers }
