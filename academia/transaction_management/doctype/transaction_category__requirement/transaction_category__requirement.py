# Copyright (c) 2024, SanU Development Team and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TransactionCategoryRequirement(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		file_type: DF.Literal["", "Image", "Document"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		required: DF.Check
		requirement_name: DF.Data
	# end: auto-generated types
	pass
