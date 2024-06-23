# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class StudentGroupTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.student_group_student.student_group_student import StudentGroupStudent
		from frappe.types import DF

		based_on: DF.Literal["", "By Sex", "All"]
		capacity: DF.Int
		faculity: DF.Link
		program: DF.Link
		student_batch: DF.Link
		students: DF.Table[StudentGroupStudent]
		tolerance: DF.Int
	# end: auto-generated types
	
	@frappe.whitelist()
	def get_students(self):

		# doctype = frappe.get_doc('DocType', 'Student Group Tool')
		# doctype.append('fields', {
		# 	'fieldname': 'ssssss',
		# 	'fieldtype': 'Data',
		# 	'label': 'ssssss'
		# })
		# doctype.save()
		# frappe.db.commit()
		students = []

		if not self.based_on:
			frappe.throw(_("Mandatory field - Based On"))
		elif not self.program:
			frappe.throw(_("Mandatory field - Program"))
		elif not self.student_batch:
			frappe.throw(_("Mandatory field - Student Batch"))
		elif not self.capacity:
			frappe.throw(_("Mandatory field - Capacity"))
		elif not self.tolerance:
			frappe.throw(_("Mandatory field - Tolerance"))
		else:
			program_enrollment = frappe.get_list('Program Enrollment', fields='*')
			for student in program_enrollment:
				if student['program'] == self.program and student['student_batch'] == self.student_batch:
					students.append(student)
		
		if not students:
			frappe.throw(_("No students Found"))
		else:
			return students

	
		
