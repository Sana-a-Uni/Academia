# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.share import add


class TransactionNew(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transactions.doctype.sub_transactions.sub_transactions import SubTransactions
		from academia.transactions.doctype.transaction_related_documents.transaction_related_documents import TransactionRelatedDocuments
		from frappe.types import DF

		amended_from: DF.Link | None
		company: DF.Link | None
		is_sub_transaction: DF.Check
		naming_series: DF.Literal["TRA-.YY.-.MM.-"]
		parent_transaction: DF.Link | None
		related_documents: DF.Table[TransactionRelatedDocuments]
		start_date: DF.Date | None
		status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
		sub_transactions: DF.Table[SubTransactions]
		title: DF.Data
		transaction_holder: DF.Link | None
	# end: auto-generated types
	def before_submit(self):
		self.start_date = frappe.utils.today()


@frappe.whitelist()
def get_shared_transactions(user):
    shared_transactions = frappe.get_all('DocShare', filters={'user': user, 'share_doctype': 'Transaction New'}, fields=['share_name'])
    transaction_names = [transaction['share_name'] for transaction in shared_transactions]
    return transaction_names

@frappe.whitelist()
def set_permissions_for_transaction(transaction_name, user_id):
    # Add share permissions to the new user
    add(
        doctype="Transaction New",
        name=transaction_name,
        user=user_id,
        read=1,
        write=1,
        share=1,
        submit=1
    )