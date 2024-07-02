# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class GroupAssignmentTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.group_assignment_group.group_assignment_group import GroupAssignmentGroup
		from frappe.types import DF

		academic_term: DF.Link
		academic_year: DF.Link
		courses: DF.Table[GroupAssignmentGroup]
		faculty: DF.Link
		group: DF.Link
		level: DF.Data | None
		program: DF.Link
		student_batch: DF.Link
	# end: auto-generated types
	
	@frappe.whitelist()
	def get_courses(self):
		courses = []

		if not self.academic_year:
			frappe.throw(_("Mandatory field - Academic Year"))
		elif not self.academic_term:
			frappe.throw(_("Mandatory field - Academic Term"))
		elif not self.program:
			frappe.throw(_("Mandatory field - Program"))
		elif not self.student_batch:
			frappe.throw(_("Mandatory field - Student Batch"))
		else:
			course_study = frappe.get_list('Course Study', fields='*')
			for course in course_study:
				if course['program'] == self.program and course['student_batch'] == self .student_batch and course['level'] == self.level and course['academic_year'] == self.academic_year and course['academic_term'] == self.academic_term:
					courses.append(course)

		if not courses:
			frappe.throw(_("No courses Found"))
		else:
			return courses

	@frappe.whitelist()
	def generate(self):
		frappe.msgprint('generate...')
