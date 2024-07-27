# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PromotionSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_rank: DF.Link | None
		naming_series: DF.Literal["ACAD-FM-S-.YYYY.-.MM.-.####."]
		next_academic_rank: DF.Link | None
		publications_count: DF.Int
		required_period_for_promotion: DF.Data | None
		required_scientific_degree: DF.Link | None
	# end: auto-generated types
	pass
