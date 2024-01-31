# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SessionMember(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		attendance: DF.Literal["Attend", "\u0650Absent"]
		member: DF.Link
		name1: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		role: DF.Literal["Head", "Rapporteur", "Member"]
	# end: auto-generated types
	pass
