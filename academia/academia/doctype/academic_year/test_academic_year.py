# Copyright (c) 2023, SanU and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestAcademicYear(FrappeTestCase):
	def test_date_validation(self):
		year = frappe.get_doc(
			{
				"doctype": "Academic Year",
				"year_start_date": "13-02-2024",
				"year_end_date": "27-01-2024",
			}
		)
		self.assertRaises(frappe.ValidationError, year.insert)
