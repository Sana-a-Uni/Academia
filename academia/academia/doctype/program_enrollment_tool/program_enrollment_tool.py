# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import json

import frappe
from frappe.model.document import Document


class ProgramEnrollmentTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from academia.academia.doctype.temporary_student_temporary.temporary_student_temporary import (
			StudentTemporaryStudent,
		)

		academic_term: DF.Link
		academic_year: DF.Link
		faculty: DF.Link
		level: DF.Link | None
		program: DF.Link
		student_batch: DF.Link
		students: DF.Table[StudentTemporaryStudent]
	# end: auto-generated types


@frappe.whitelist()
def enroll_students(doc: str):
	doc = frappe.parse_json(doc)
	# Fetch the specified program from the parent document

	# Fetch students from the child table
	students = doc.get("students")  # Ensure this matches your child table field name

	for student in students:
		# Create a new enrollment document for each student
		enrollment = frappe.get_doc(
			{
				"doctype": "Program Enrollment",  # Ensure this is the correct DocType
				"student": student["student_id"],  # Ensure this is the right field for student reference
				"academic_year": doc.academic_year,  # Field from the parent DocType
				"academic_term": doc.academic_term,  # Field from the parent DocType
				"student_batch": doc.student_batch,  # Field from the parent DocType
				"faculty": doc.faculty,  # Field from the parent DocType
				"program": doc.program,  # Field from the parent DocType
				# Include any other necessary fields
			}
		)

		# Insert the new enrollment document
		enrollment.insert(ignore_permissions=True)

	# Commit the changes
	frappe.db.commit()
