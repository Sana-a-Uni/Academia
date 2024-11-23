# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TemporaryStudentTemporary(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		first_name: DF.Data | None
		gender: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		student_name: DF.Data | None
	# end: auto-generated types
	pass
