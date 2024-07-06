# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TransactionCategoryTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transaction_management.doctype.transaction_template_fields.transaction_template_fields import TransactionTemplateFields
		from frappe.types import DF

		description: DF.TextEditor | None
		linked_fields: DF.Table[TransactionTemplateFields]
		template_title: DF.Data | None
	# end: auto-generated types
	pass
