# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class TransactionAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_date: DF.Datetime | None
		amended_from: DF.Link | None
		created_by: DF.Link | None
		details: DF.Text | None
		from_company: DF.Data | None
		from_department: DF.Data | None
		from_designation: DF.Data | None
		redirected_to: DF.Link | None
		to_company: DF.Link | None
		to_department: DF.DynamicLink | None
		to_party: DF.Link | None
		transaction: DF.Link | None
		type: DF.Literal["Received", "Redirected", "Approved", "Rejected", "Canceled", "Council"]
	# end: auto-generated types
	pass


@frappe.whitelist()
def get_transaction_actions(transaction_name):
    """
    Retrieves all the Transaction Action documents associated with the given Transaction document.
    
    Args:
        transaction_name (str): Name of the Transaction document.
        
    Returns:
        List[dict]: List of dictionaries representing the Transaction Action documents.
    """
    transaction_actions = frappe.db.get_all(
        "Transaction Action",
        filters={
            "transaction": transaction_name
        },
        fields=["name", "type", "redirected_to", "details", "action_date"],
		order_by="action_date DESC",
    )
    
    return transaction_actions
