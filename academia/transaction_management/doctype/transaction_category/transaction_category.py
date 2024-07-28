# Copyright (c) 2024, SanU Development Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TransactionCategory(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transaction_management.doctype.transaction_category__requirement.transaction_category__requirement import TransactionCategoryRequirement
		from academia.transaction_management.doctype.transaction_recipients.transaction_recipients import TransactionRecipients
		from frappe.types import DF

		category_name: DF.Data
		company: DF.Link | None
		is_group: DF.Check
		parent_category: DF.Link | None
		recipients: DF.Table[TransactionRecipients]
		requirements: DF.Table[TransactionCategoryRequirement]
		template: DF.Link | None
	# end: auto-generated types
	pass


# I used the one in transaction.py
# @frappe.whitelist()
# def get_transaction_category_requirement(transaction_category):
#     requirements = frappe.get_all("Transaction Category  Requirement",
#                                    filters={"parent": transaction_category},
#                                    fields=["name", "file_type", "required"])
#     return requirements


    	
        	
            	
