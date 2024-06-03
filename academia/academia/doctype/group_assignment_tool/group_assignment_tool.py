# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class GroupAssignmentTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.group_assignment_group.group_assignment_group import GroupAssignmentGroup
		from frappe.types import DF

		academic_term: DF.Link
		academic_year: DF.Link
		faculty: DF.Link
		group: DF.Data
		program: DF.Link
		student_batch: DF.Link
		table_acya: DF.Table[GroupAssignmentGroup]
	# end: auto-generated types
	pass
