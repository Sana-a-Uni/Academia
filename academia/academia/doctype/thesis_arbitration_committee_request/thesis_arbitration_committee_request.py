# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ThesisArbitrationCommitteeRequest(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.external_discussion_committee.external_discussion_committee import ExternalDiscussionCommittee
		from academia.academia.doctype.internal_discussion_committee.internal_discussion_committee import InternalDiscussionCommittee
		from frappe.types import DF

		amended_from: DF.Link | None
		external_arbitration_committee: DF.Table[ExternalDiscussionCommittee]
		faculty_member: DF.Link | None
		faculty_member_publication: DF.Link | None
		internal_arbitration_committee: DF.Table[InternalDiscussionCommittee]
		modified_request_date: DF.Date | None
		naming_series: DF.Literal["ACAD-TDC-REQ-.YY.-.MM.-.#####."]
		rejection_reason: DF.SmallText | None
		request_attachment: DF.Attach | None
		request_date: DF.Date | None
		status: DF.Data | None
		supervisor_name: DF.Link | None
	# end: auto-generated types
	pass
