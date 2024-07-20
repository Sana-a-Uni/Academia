# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime

def execute(filters=None):
	columns = [
		"Transaction", "Company", "Department", "Employee", "Start Date"
	]

	data = []

	transaction_type = filters.filter_type
	company = filters.filter_company
	department = filters.filter_department

	my_filters = {}
	
	if transaction_type == "outgoing":
		if company:
			my_filters["start_with_company"] = company

		if department:
			my_filters["start_with_department"] = department

		transactions = frappe.db.get_all("Transaction", filters=my_filters, fields=["name", "start_with_company", "start_with_department", "start_from_employee", "start_with", "creation"])

		for transaction in transactions:
			creation_date = transaction.creation.strftime("%d/%m/%y (%H:%M)")
			data.append([
				transaction.name,
				transaction.start_with_company,
				transaction.start_with_department,
				transaction.start_from_employee,
				creation_date
			])

		return columns, data
	
	else:

		transactions = frappe.db.get_all(
			"Transaction", 
			filters={
				"transaction_scope": not "With External Entity",
				"circular": 0
			}, 
			fields=["name", "start_with_company", "start_with_department", "start_from_employee", "start_with", "creation"])
		
		for transaction in transactions:

			if company:
				my_filters["recipient_company"] = company

			if department:
				my_filters["recipient_department"] = department
			
			my_filters["parent"] = transaction.name

			transaction_recipients = frappe.db.get_all(
				"Transaction Recipients", 
				filters=my_filters, 
				fields=["name", "recipient_name", "recipient_company", "recipient_department", "recipient_email"]
			)
		
			if transaction_recipients:
				for trans_recip in transaction_recipients:
					creation_date = transaction.creation.strftime("%d/%m/%y (%H:%M)")
					data.append([
						transaction.name,
						trans_recip.recipient_company,
						trans_recip.recipient_department,
						trans_recip.recipient_name,
						creation_date
					])

		return columns, data

		