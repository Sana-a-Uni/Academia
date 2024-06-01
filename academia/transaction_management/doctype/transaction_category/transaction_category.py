# Copyright (c) 2024, SanU Development Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TransactionCategory(Document):
	pass


# I used the one in transaction.py
# @frappe.whitelist()
# def get_transaction_category_requirement(transaction_category):
#     requirements = frappe.get_all("Transaction Category  Requirement",
#                                    filters={"parent": transaction_category},
#                                    fields=["name", "file_type", "required"])
#     return requirements


    	
        	
            	
