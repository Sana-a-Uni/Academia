# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class OutboxMemoAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import (
			TransactionRecipientsNew,
		)

		action_date: DF.Data | None
		amended_from: DF.Link | None
		created_by: DF.Link | None
		details: DF.Text | None
		employee_name: DF.Data | None
		from_company: DF.Data | None
		from_department: DF.Data | None
		from_designation: DF.Data | None
		outbox_memo: DF.Link
		recipients: DF.Table[TransactionRecipientsNew]
		start_from: DF.Link | None
		type: DF.Literal["Redirected", "Approved", "Rejected", "Canceled"]
	# end: auto-generated types
	pass
