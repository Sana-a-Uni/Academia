# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TransactionRelatedDocuments(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		document_name: DF.DynamicLink | None
		document_title: DF.Data | None
		document_type: DF.Literal["Outbox Memo", "Inbox Memo", "Request", "Specific Transaction Document"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types
	pass