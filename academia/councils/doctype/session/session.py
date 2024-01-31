# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Session(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.councils.doctype.session_member.session_member import SessionMember
		from academia.councils.doctype.session_topic_assignment.session_topic_assignment import SessionTopicAssignment
		from frappe.types import DF

		amended_from: DF.Link | None
		begin_time: DF.Time | None
		council: DF.Link
		date: DF.Date | None
		end_time: DF.Time | None
		members: DF.Table[SessionMember]
		naming_series: DF.Literal["CNCL-SESS-.YY.-.{council}.-.###"]
		opening: DF.Text
		title: DF.Data
		topics: DF.Table[SessionTopicAssignment]
	# end: auto-generated types
	pass
