# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StudentBatch(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		batch_name: DF.Data
		current_level: DF.Link | None
		program: DF.Link
		program_specification: DF.Link
		status: DF.Literal["", "Continue", "Finished"]
	# end: auto-generated types
	pass
