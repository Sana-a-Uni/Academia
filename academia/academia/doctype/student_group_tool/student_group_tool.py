# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StudentGroupTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.student_group_student.student_group_student import StudentGroupStudent
		from frappe.types import DF

		based_on: DF.Literal["", "By Sex", "All"]
		max_strength: DF.Int
		student_batch: DF.Link
		table_yldo: DF.Table[StudentGroupStudent]
	# end: auto-generated types
	pass
