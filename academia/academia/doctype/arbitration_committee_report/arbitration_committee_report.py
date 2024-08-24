# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ArbitrationCommitteeReport(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		date: DF.Date | None
		report_author: DF.Link | None
		report_content: DF.TextEditor | None
		report_file: DF.Attach | None
		report_title: DF.Data | None
	# end: auto-generated types
	pass
