# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt
from frappe import _
import frappe
from frappe.model.document import Document


class TopicApplicant(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		applicant: DF.DynamicLink
		applicant_type: DF.Literal["", "Student", "Faculty Member", "Employee", "Other"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data

	# end: auto-generated types
	@property
	def applicant_name(self):
		name_fields_mapping = {
			"Student": ["first_name", "last_name"],
			"Faculty Member": ["faculty_member_name"],
			"Employee": ["employee_name"],
		}
		name_fields = name_fields_mapping.get(self.applicant_type, [])
		if not name_fields:
			return _("Name Not Set")
		# Fetch both 'first_name' and 'last_name' in one database call
		fields = frappe.get_value(self.applicant_type, self.applicant, name_fields, as_dict=1)

		if fields:
			if self.applicant_type == "Student":
				# Combine first and last name to form full name
				return f"{fields.get('first_name', '')} {fields.get('last_name', '')}".strip()
			else:
				# Return the single name field for other types
				for field in name_fields:
					return fields.get(field, _("Name Not Set"))
		else:
			# Handle cases where no data is found
			return _("Name Not Set")
