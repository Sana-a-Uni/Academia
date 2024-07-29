# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta


def format_timedelta(td):
    """Helper function to format a timedelta object into a string"""
    days, remainder = divmod(td.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"


def execute(filters=None):
	columns = [
        "Transaction", "Transaction Company", "Transaction Department", "Employee", "Employee Company", "Employee Department", "Expected Time", "Real Taken Tim", "Difference Time", "Is Transaction Completed"
    ]
 
	# Fetch all relevant data
	my_filters = {"circular": 0, "docstatus": 1}
    
	if filters.filter_company:
		my_filters["start_with_company"] = filters.filter_company
	if filters.filter_department:
		my_filters["start_with_department"] = filters.filter_department
	if filters.filter_category:
		my_filters["category"] = filters.filter_category

	# Fetch all relevant data
	transactions = frappe.db.get_all(
		"Transaction",
		filters=my_filters, 
		fields=["name", "start_with", "start_with_company", "start_with_department", "creation", "submit_time", "complete_time"],
		order_by="creation",
	)

	
	
	settings = frappe.get_all("Transaction Settings", fields=["company", "department", "step_duration"])
	settings_map = {(setting.company, setting.department): setting.step_duration for setting in settings}

	data = []
	if (filters.filter_employee):
		employee_in_filter= frappe.get_doc("Employee", filters.filter_employee)
		user_id_employee_in_filter = employee_in_filter.user_id

	for transaction in transactions:
		key = (transaction.start_with_company, transaction.start_with_department)
		if key in settings_map:
			step_duration = settings_map[key]
			step_duration_timedelta = timedelta(seconds=float(step_duration))

			actions = frappe.db.get_all(
				"Transaction Action", 
				filters={"transaction":transaction.name, "docstatus": 1, "type": not "Canceled"}, 
				fields=["name", "transaction", "type", "owner", "from_company", "from_department", "creation"],
				order_by="creation",
			)

			is_transaction_completed = transaction.complete_time

			if actions:
				last_action = actions[-1]
				prev_action_creation = actions[0].creation
				for i in range(1, len(actions)):
					# last_action = actions[i]
					curr_action_creation = actions[i].creation
					real_taken_time = curr_action_creation - prev_action_creation
					is_transaction_completed = transaction.complete_time
					
					if not filters.filter_employee or (user_id_employee_in_filter == actions[i].owner):

						if real_taken_time > step_duration_timedelta:
							difference_time = real_taken_time - step_duration_timedelta
							late_employee = frappe.get_doc("Employee", {"user_id": actions[i].owner})
							
							row = [
								transaction.name,
								transaction.start_with_company,
								transaction.start_with_department,
								late_employee.employee_name,
								late_employee.company,
								late_employee.department,
								format_timedelta(step_duration_timedelta),
								format_timedelta(real_taken_time),
								format_timedelta(difference_time),
								"Yes" if is_transaction_completed else "No"
							]
							data.append(row)
					
					prev_action_creation = curr_action_creation
				
				# if not filters.filter_employee or (user_id_employee_in_filter == last_action.owner):
					# check the last action
					
					# if (not is_transaction_completed):
				doc_shares= frappe.get_all(
					"DocShare",
					filters={"share_doctype": "Transaction", "share_name": transaction.name,},
					fields=["name", "user", "creation"],
					order_by='creation',
				)
				last_doc_share = doc_shares[-1]
				if not filters.filter_employee or (user_id_employee_in_filter == last_doc_share.user):
					late_employee = frappe.get_doc("Employee", {"user_id": last_doc_share.user})
					if(is_transaction_completed):
						real_taken_time = transaction.complete_time - last_doc_share.creation
					else:
						real_taken_time = datetime.now() - last_doc_share.creation
					if(real_taken_time > step_duration_timedelta):
						difference_time = real_taken_time - step_duration_timedelta
						row = [
							transaction.name,
							transaction.start_with_company,
							transaction.start_with_department,
							late_employee.employee_name,
							late_employee.company,
							late_employee.department,
							format_timedelta(step_duration_timedelta),
							format_timedelta(real_taken_time),
							format_timedelta(difference_time),
							"Yes" if is_transaction_completed else "No"
						]
						data.append(row)

	return columns, data
