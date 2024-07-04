# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StudentGroup(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.student_group_student.student_group_student import StudentGroupStudent
		from frappe.types import DF

		batch: DF.Link | None
		faculty: DF.Link | None
		group_based_on: DF.Data
		program: DF.Link | None
		student_group_name: DF.Data
		students1: DF.Table[StudentGroupStudent]
		students2: DF.Table[StudentGroupStudent]
		students3: DF.Table[StudentGroupStudent]
		students: DF.Table[StudentGroupStudent]
	# end: auto-generated types
	pass
