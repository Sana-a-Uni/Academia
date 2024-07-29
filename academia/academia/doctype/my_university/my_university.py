# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MyUniversity(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		abbr: DF.Data
		city: DF.Data
		country: DF.Link
		date_of_establishment: DF.Date
		description: DF.TextEditor | None
		email: DF.Data | None
		fax: DF.Data | None
		phone_no: DF.Phone | None
		private: DF.Check
		university__mission: DF.TextEditor | None
		university_goals: DF.TextEditor | None
		university_logo: DF.AttachImage | None
		university_name: DF.Data
		university_name_english: DF.Data
		university_vision: DF.TextEditor | None
		website: DF.Data | None
	# end: auto-generated types
	pass
