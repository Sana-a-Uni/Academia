# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TransactionPaperLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_name: DF.Link | None
		middle_man: DF.Link | None
		through_middle_man: DF.Check
		to: DF.Link | None
		transaction_name: DF.Link | None
	# end: auto-generated types
	pass
