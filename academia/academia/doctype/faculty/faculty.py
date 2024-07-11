# Copyright (c) 2023, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Faculty(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		abbr: DF.Data
		company: DF.Link
		current_academic_term: DF.Link | None
		current_academic_year: DF.Link | None
		date_of_establishment: DF.Data
		default_holiday_list: DF.Data
		description: DF.TextEditor | None
		email: DF.Data | None
		faculty_goals: DF.TextEditor | None
		faculty_logo: DF.AttachImage | None
		faculty_mission: DF.TextEditor | None
		faculty_name: DF.Data
		faculty_vision: DF.TextEditor | None
		fax: DF.Data | None
		is_group: DF.Check
		is_research_center: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_faculty: DF.Link | None
		phone_no: DF.Phone | None
		rgt: DF.Int
		website: DF.Data | None
	# end: auto-generated types
	pass
