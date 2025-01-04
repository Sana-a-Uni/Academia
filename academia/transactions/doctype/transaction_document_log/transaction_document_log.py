# Copyright (c) 2025, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TransactionDocumentLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from academia.transaction_management.doctype.transaction_attachments.transaction_attachments import (
			TransactionAttachments,
		)

		amended_from: DF.Link | None
		attachments: DF.Table[TransactionAttachments]
		document_action_name: DF.DynamicLink | None
		document_action_type: DF.Literal[
			"Inbox Memo Action",
			"Outbox Memo Action",
			"Request Action",
			"Specific Transaction Document Action",
		]
		document_name: DF.DynamicLink | None
		document_type: DF.Literal["Inbox Memo", "Outbox Memo", "Request", "Specific Transaction Document"]
		ee_proof: DF.Attach | None
		end_employee: DF.Link | None
		end_employee_name: DF.Data | None
		middle_man: DF.Link | None
		middle_man_name: DF.Data | None
		mm_proof: DF.Attach | None
		paper_progress: DF.Literal[
			"",
			"Delivered to middle man",
			"Received by middle man",
			"Delivered to end employee",
			"Received by end employee",
		]
		start_employee: DF.Link | None
		start_employee_name: DF.Data | None
		through_middle_man: DF.Check
	# end: auto-generated types
	pass


@frappe.whitelist()
def change_is_received(doctype: str, docname: str, is_received: bool):
	doc = frappe.get_doc(doctype, docname)
	doc.is_received = is_received
	doc.save()
	frappe.db.commit()
	return doc
