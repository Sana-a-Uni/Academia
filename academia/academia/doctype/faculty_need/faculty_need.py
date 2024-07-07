# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FacultyNeed(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_specialty: DF.Link | None
		academic_year: DF.Link | None
		amended_from: DF.Link | None
		department: DF.Link | None
		faculty_position: DF.Int
		scientific_degree: DF.Link | None
	# end: auto-generated types
	pass
