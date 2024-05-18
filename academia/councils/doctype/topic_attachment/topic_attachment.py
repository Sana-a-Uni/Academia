# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TopicAttachment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		attachment: DF.Attach
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		title: DF.Data
		type: DF.Literal["", "Supporting Document", "Minutes", "Document", "Image", "Report"]
		upload_date: DF.Date | None
	# end: auto-generated types
	pass
