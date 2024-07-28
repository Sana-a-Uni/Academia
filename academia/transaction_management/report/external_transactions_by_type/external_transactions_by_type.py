# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	if filters.filter_type:
		my_filters = {}
		
		my_filters['transaction_scope'] = "With External Entity"
		my_filters['type'] = filters.filter_type
		
		transactions = frappe.db.get_all("Transaction", filters=my_filters, fields=["name", "start_with_company", "start_with_department", "start_from_employee", "start_with", "creation", "reference_transaction", "main_external_entity_from", "sub_external_entity_from", "main_external_entity_to", "sub_external_entity_to"])

		data = []

		if filters.filter_type == 'Outgoing':
			columns = [
				"Transaction", "Refrenced Transaction", "From Company", "Department", "To Main External Entity", "To Sub External Entity", "Employee", "Start Date"
			]
			
			for transaction in transactions:
				creation_date = transaction.creation.strftime("%d/%m/%y (%H:%M)")
				data.append([
					transaction.name,
					transaction.reference_transaction,
					transaction.start_with_company,
					transaction.start_with_department,
					transaction.main_external_entity_to,
					transaction.sub_external_entity_to,
					transaction.start_from_employee,
					creation_date
				]) 
			
		else:
			columns = [
				"Transaction", "From Main External Entity", "Sub External Entity", "To Company", "To Department", "Start Date"
			]

			for transaction in transactions:
				creation_date = transaction.creation.strftime("%d/%m/%y (%H:%M)")

				transaction_recipients = frappe.db.get_all(
					"Transaction Recipients", 
					filters={"parent": transaction.name}, 
					fields=["name", "recipient_name", "recipient_company", "recipient_department", "recipient_email"]
				)

				if transaction_recipients:
					trans_recip = transaction_recipients[0]
					to_company = trans_recip.recipient_company if trans_recip.recipient_company else ''
					to_department = trans_recip.recipient_department if trans_recip.recipient_department else ''

					data.append([
						transaction.name,
						transaction.main_external_entity_from,
						transaction.sub_external_entity_from,
						to_company,
						to_department,
						creation_date
					])
				else:
					data.append([
						transaction.name,
						transaction.main_external_entity_from,
						transaction.sub_external_entity_from,
						'',
						'',
						creation_date
					])


		



	
	return columns, data
