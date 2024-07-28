# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class DepartmentNeed(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_specialty: DF.Link | None
		academic_year: DF.Link
		amended_from: DF.Link | None
		faculty: DF.Link
		faculty_department: DF.Link
		naming_series: DF.Literal["DEPTND-.department.-.academic_year.-"]
		number_of_positions: DF.Data
		scientific_degree: DF.Link
		specialist_field: DF.Data | None
	# end: auto-generated types
	pass

	def validate(self):
		self.validate_number_of_positions()

	def validate_number_of_positions(self):
		if self.number_of_positions and not re.match("^[0-9]+$", str(self.number_of_positions)):
			frappe.throw("Number of Positions should only contain numbers")
    