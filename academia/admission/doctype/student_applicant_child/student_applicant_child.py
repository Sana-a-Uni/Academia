# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StudentApplicantChild(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		faculty: DF.Data | None
		faculty_department: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		program_degree: DF.Data | None
		student_email_address: DF.Data | None
		student_name: DF.Data | None
	# end: auto-generated types
	pass
