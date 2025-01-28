# Copyright (c) 2025, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EmployeeProxy(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transactions.doctype.delegated_employees.delegated_employees import DelegatedEmployees
		from frappe.types import DF

		delegated_employees: DF.Table[DelegatedEmployees]
		employee: DF.Link | None
		employee_company: DF.Link
		employee_department: DF.Link
		employee_designation: DF.Link
		employee_email: DF.Link | None
		employee_name: DF.Data | None
	# end: auto-generated types
	pass
