# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SessionTopic(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		decision: DF.TextEditor | None
		decision_type: DF.Literal["Other", "Accepted", "Rejected"]
		description: DF.TextEditor | None
		get_template: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		status: DF.Literal["", "Postponed", "Resolved"]
		title: DF.Data | None
		topic: DF.Link
	# end: auto-generated types
	pass

	@property
	def description(self):
		return frappe.get_value("Topic", self.topic, "description")

	@property
	def title(self):
		return frappe.get_value("Topic", self.topic, "title")
