# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InboxMemoAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import TransactionRecipientsNew
		from frappe.types import DF

		action_date: DF.Date
		amended_from: DF.Link | None
		created_by: DF.Data | None
		details: DF.Text | None
		from_company: DF.Link | None
		from_department: DF.Link | None
		from_designation: DF.Link | None
		inbox_memo: DF.Link
		recipients: DF.Table[TransactionRecipientsNew]
		type: DF.Literal["Redirected", "Approved", "Rejected", "Canceled", "Topic"]
	# end: auto-generated types
	def on_submit(self):
		self.action_date = frappe.utils.now()
		self.created_by = self.owner

		# make a read, write, share permissions for reciepents
		user = frappe.get_doc("User", self.recipients[0].recipient_email)
		frappe.share.add(
			doctype="Inbox Memo",
			name=self.inbox_memo,
			user=user.email,
			read=1,
			write=1,
			share=1,
			submit=1,
		)
		
