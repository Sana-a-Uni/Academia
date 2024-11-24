# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ProgramEnrollmentTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from academia.academia.doctype.temporary_student_temporary.temporary_student_temporary import (
			TemporaryStudentTemporary,
		)

		academic_term: DF.Link | None
		academic_year: DF.Link | None
		faculty: DF.Link | None
		level: DF.Link | None
		progarm: DF.Link | None
		student_batch: DF.Link | None
		students: DF.Table[TemporaryStudentTemporary]
	# end: auto-generated types
	pass
