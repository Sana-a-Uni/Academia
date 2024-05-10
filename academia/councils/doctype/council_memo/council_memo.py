# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CouncilMemo(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		council: DF.Link
		current_assignment: DF.Link
		description: DF.TextEditor | None
		memo_date: DF.Date
		naming_series: DF.Literal["CNCL-CM-.{assignmet}.##"]
		next_assignment: DF.Link | None
		title: DF.Data
	# end: auto-generated types
	pass
