# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TransactionPaperLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_name: DF.Link | None
		amended_from: DF.Link | None
		end_employee: DF.Link | None
		end_employee_name: DF.Data | None
		middle_man: DF.Link | None
		middle_man_name: DF.Data | None
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
		transaction_name: DF.Link | None
	# end: auto-generated types
	pass


# @frappe.whitelist()
# def received_middle_man(doc):
# 	doc.paper_progress = "Received by middle man"
# 	return "Received by middle man"

# # @frappe.whitelist()
# # def delivered_middle_man(doc):
# # 	doc.paper_progress = "Delivered by middle man"
# # 	return "Delivered by middle man"

# # @frappe.whitelist()
# # def received_end_employee(doc):
# # 	doc.paper_progress = "Received by end employee"
# # 	return "Received by end employee"

frappe.whitelist()


def give_permission_to_end_employee(doc, end_employee):
	end_employee_email = frappe.get_value("Employee", end_employee, "user_id") if end_employee else None

	# Share the document with the end employee
	frappe.share.add(
		doctype="Transaction Paper Log",
		name=doc.name,
		user=end_employee_email,
		read=1,
		write=1,
		share=1,
	)
