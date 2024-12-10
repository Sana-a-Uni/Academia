# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class TemporaryImportStudent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_term: DF.Data
		academic_year: DF.Data
		faculty: DF.Data
		first_name: DF.Data
		gender: DF.Data
		program: DF.Data
		student_batch: DF.Data
		student_id: DF.Data
		student_name: DF.Data | None
	# end: auto-generated types


@frappe.whitelist()
def enroll_students():
	# Fetch all records from Temporary Import Student
	temporary_students = frappe.get_all("Temporary Import Student", fields=["*"])

	for temp_student in temporary_students:
		# Create a new Student record
		student = frappe.get_doc(
			{
				"doctype": "Student",
				"first_name": temp_student.first_name,
				"last_name": temp_student.last_name,
				"email": temp_student.email,
				"gender": temp_student.gender,
				# Add other necessary fields
			}
		)
		student.insert()
		frappe.db.commit()

		# Create a new Program Enrollment record
		program_enrollment = frappe.get_doc(
			{
				"doctype": "Program Enrollment",
				"student": student.name,
				"program": temp_student.program,
				"faculty": temp_student.faculty,
				"student_batch": temp_student.student_batch,
				"academic_year": temp_student.academic_year,
				"academic_term": temp_student.academic_term,
				# Add other necessary fields
			}
		)
		program_enrollment.insert()
		frappe.db.commit()

		# Delete the temporary student record
		frappe.delete_doc("Temporary Import Student", temp_student.name)
		frappe.db.commit()

	frappe.msgprint(_("Students have been successfully enrolled."))
