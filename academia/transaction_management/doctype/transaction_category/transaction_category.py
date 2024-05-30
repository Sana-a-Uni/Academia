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
		from frappe.types import DF

		category_name: DF.Data
		category_parent: DF.Link | None
		requirements: DF.Table[TransactionCategoryRequirement]
		text_editor_uzrj: DF.TextEditor | None
	# end: auto-generated types
	pass

    	
        	
            	
