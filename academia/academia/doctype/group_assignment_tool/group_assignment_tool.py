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
		group: DF.Data
		program: DF.Link
		student_batch: DF.Link
	# end: auto-generated types
	
	@frappe.whitelist()
	def get_courses(self):
		frappe.msgprint('get_courses...')

	@frappe.whitelist()
	def generate(self):
		frappe.msgprint('generate...')
