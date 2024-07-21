# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta


def execute(filters=None):
	columns = [
        "Transaction", "Company", "Department", "Employee", "Duration Exceeded", "Time Difference (Minutes)"
    ]

	data = []

	# Fetch all relevant data
	transactions = frappe.db.get_all(
		"Transaction",
		filters={"circular": 0, "docstatus": 1,}, 
		fields=["name", "start_with", "start_with_company", "start_with_department"],
		order_by="creation",
	)
	redirected_actions = frappe.db.get_all(
		"Transaction Action", 
		filters={"type": "Redirected", "docstatus": 1,}, 
		fields=["name", "transaction", "type", "owner", "from_company", "from_department", "creation"],
		order_by="creation",
	)
	actions = frappe.db.get_all(
		"Transaction Action", 
			filters={"docstatus": 1,}, 
			fields=["name", "transaction", "type", "owner", "from_company", "from_department", "creation"],
			order_by="creation",
		)
	settings = frappe.db.get_all(
		"Transaction Settings", 
		fields=["company", "department", "duration"],
	)


	for transaction in transactions:
		checked_actions = []

		if transaction.start_with_company and transaction.start_with_department:
			setting = frappe.get_doc(
				"Transaction Settings", 
				{"company": transaction.start_with_company, "department": transaction.start_with_department}
			)
			duration_setting = setting.duration
		
		all_actions = frappe.db.get_all(
			"Transaction Action", 
				filters={"docstatus": 1,}, 
				fields=["name", "transaction", "type", "owner", "from_company", "from_department", "creation"],
				order_by="creation",
		)

		for action in all_actions:
			if action.name not in checked_actions:
				if action.type == "Approved" or action.type == "Rejected":
					time_difference = ""


	# data.append([
	#     transaction.name,
	#     transaction.start_with_company,
	#     transaction.start_with_department,
	#     "Yes" if duration_exceeded else "No",
	#     time_diff_minutes
	# ])

	return columns, data
