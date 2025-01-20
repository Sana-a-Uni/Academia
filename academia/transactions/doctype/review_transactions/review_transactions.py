# Copyright (c) 2025, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ReviewTransactions(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transactions.doctype.transactions_for_review.transactions_for_review import TransactionsForReview
		from frappe.types import DF

		amended_from: DF.Link | None
		current_action_maker: DF.Data | None
		document_content: DF.TextEditor | None
		naming_series: DF.Literal["RT-.YY.-.MM.-"]
		start_from: DF.Link
		start_from_company: DF.Link
		start_from_department: DF.Link | None
		start_from_designation: DF.Link | None
		start_from_employee: DF.Data
		status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
		title: DF.Data
		transaction_reference: DF.Link
		transactions_for_review: DF.Table[TransactionsForReview]
	# end: auto-generated types
	pass

@frappe.whitelist()
def get_documents(filters):
    # Dynamically fetch documents based on the document_type
    document_type = filters.get('document_type')

    # You can add a dictionary to map document types to their corresponding Doctype names
    doctype_map = {
        "Outbox Memo": "Outbox Memo",
        "Inbox Memo": "Inbox Memo",
        "Request": "Request",
        "Specific Transaction Document": "Specific Transaction Document"
    }

    # Get the actual Doctype based on the document_type
    doctype = doctype_map.get(document_type)

    if not doctype:
        return []  # Return an empty list if the document_type is invalid

    # Fetch documents based on the Doctype and other filters
    return frappe.get_all(
        doctype,
        fields=["name", "title"],  # Adjust fields as necessary
        filters={
            "docstatus": 1,  # Only submitted documents
        }
    )
