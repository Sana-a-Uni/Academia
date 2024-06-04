# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SessionTopicAssignment(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        council_memo: DF.Link | None
        decision: DF.TextEditor | None
        decision_type: DF.Literal["", "Postponed", "Resolved", "Transferred"]
        description: DF.TextEditor | None
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
        title: DF.Data | None
        topic_assignment: DF.Link
    # end: auto-generated types
    pass

    @property
    def description(self):
        return frappe.get_value('Topic Assignment', self.topic_assignment, 'description')

    @property
    def title(self):
        return frappe.get_value('Topic Assignment', self.topic_assignment, 'title')
