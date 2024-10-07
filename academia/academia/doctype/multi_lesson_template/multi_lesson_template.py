# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MultiLessonTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		group: DF.Link
		level: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		program: DF.Link
	# end: auto-generated types
	pass
