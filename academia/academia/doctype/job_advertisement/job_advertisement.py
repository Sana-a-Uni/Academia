# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class JobAdvertisement(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.approved_department_need.approved_department_need import ApprovedDepartmentNeed
		from academia.academia.doctype.job_advertisement_journal.job_advertisement_journal import JobAdvertisementJournal
		from frappe.types import DF

		approved_department_needs: DF.Table[ApprovedDepartmentNeed]
		end_date: DF.Datetime | None
		general_application_terms: DF.Text | None
		job_advertisement_journal: DF.Table[JobAdvertisementJournal]
		reference_to_need_aggregation: DF.Link | None
		start_date: DF.Datetime | None
	# end: auto-generated types
	pass
