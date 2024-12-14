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
		department: DF.Data | None
		faculty: DF.Data
		first_name: DF.Data
		gender: DF.Data
		last_name: DF.Data | None
		level: DF.Data | None
		middle_name: DF.Data | None
		program: DF.Data
		student_batch: DF.Data
		student_id: DF.Data
	# end: auto-generated types


@frappe.whitelist()
def enroll_students():
    # Fetch all records from Temporary Import Student
    temporary_students = frappe.get_all("Temporary Import Student", fields=["*"])
    total_students = len(temporary_students)

    for index, temp_student in enumerate(temporary_students):
        # Create a new Student record
        student = frappe.get_doc(
            {
                "doctype": "Student",
                "first_name": temp_student.first_name,
                "middle_name": temp_student.middle_name,
                "last_name": temp_student.last_name,
                "email": temp_student.email,
                "gender": temp_student.gender,
                "current_student_id": temp_student.student_id,
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

        # Send progress update
        progress_percentage = int((index + 1) / total_students * 100)
        frappe.publish_realtime('enrollment_progress', {'percentage': progress_percentage}, user=frappe.session.user)

    # frappe.msgprint(_("Students have been successfully enrolled."))