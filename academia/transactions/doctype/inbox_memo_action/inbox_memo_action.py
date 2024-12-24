# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class InboxMemoAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import (
			TransactionRecipientsNew,
		)

		action_date: DF.Date
		amended_from: DF.Link | None
		created_by: DF.Data | None
		details: DF.TextEditor | None
		from_company: DF.Link | None
		from_department: DF.Link | None
		from_designation: DF.Link | None
		inbox_memo: DF.Link
		recipients: DF.Table[TransactionRecipientsNew]
		type: DF.Literal["Redirected", "Approved", "Rejected", "Canceled", "Topic"]
	# end: auto-generated types
	pass
