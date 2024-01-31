# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Council(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.councils.doctype.council_member.council_member import CouncilMember
		from frappe.types import DF

		administrative_body: DF.Data | None
		council_members: DF.Table[CouncilMember]
		council_name: DF.Data
	# end: auto-generated types
	pass
