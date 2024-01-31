# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TopicAssignment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.councils.doctype.topic_assignment_attachment.topic_assignment_attachment import TopicAssignmentAttachment
		from frappe.types import DF

		amended_from: DF.Link | None
		assignment_date: DF.Date
		attachments: DF.Table[TopicAssignmentAttachment]
		council: DF.Link
		decision: DF.TextEditor | None
		decision_type: DF.Literal["", "Postponed", "Resolved", "Transferred"]
		description: DF.TextEditor
		main_type: DF.Data | None
		naming_series: DF.Literal["CNCL-TA-.{topic}.##"]
		status: DF.Literal["", "Pending Review", "Pending Acceptance", "Accepted", "Rejected"]
		subtype: DF.Data | None
		title: DF.Data
		topic: DF.Link
	# end: auto-generated types
	pass
