# Copyright (c) 2022, Warehouseman and Contributors
# See license.txt

# import frappe
import unittest

class TestReturnablesBatchTransfers(unittest.TestCase):

	def setUp(self):
		frappe.set_user("Administrator")

	def tearDown(self):
		frappe.set_user("Administrator")

	def minimal(self):
		# doc = frappe.get_doc("Returnables Batch Transfers", frappe.db.get_value("Event", {"subject":"_Test Event 1"}))
		self.assertTrue( 0 == 0 )
