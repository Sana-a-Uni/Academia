# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AcademicProgram(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		courses: DF.Check
		faculty: DF.Link
		faculty_department: DF.Link
		maximum_research_period: DF.Int
		minimum_course_average_to_start_research: DF.Data | None
		minimum_research_period: DF.Int
		program_abbreviation: DF.Data
		program_degree: DF.Literal["", "Post-Secondary Diploma", "Bachelor's Degree", "Postgraduate Diploma", "Master Degree", "PHD Degree"]
		program_name: DF.Data
		research_or_thesis: DF.Check
		starrting_year_of_program: DF.Date | None
	# end: auto-generated types
	pass
