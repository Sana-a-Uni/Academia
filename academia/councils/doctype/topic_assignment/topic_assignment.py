# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _
from frappe.model.document import Document


class TopicAssignment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.councils.doctype.topic_assignment_copy.topic_assignment_copy import TopicAssignmentCopy
		from academia.councils.doctype.topic_attachment.topic_attachment import TopicAttachment
		from frappe.types import DF

		amended_from: DF.Link | None
		assignment_date: DF.Date
		attachments: DF.Table[TopicAttachment]
		council: DF.Link
		decision: DF.TextEditor | None
		decision_type: DF.Literal["", "Postponed", "Resolved", "Transferred"]
		description: DF.TextEditor
		grouped_assignments: DF.Table[TopicAssignmentCopy]
		is_group: DF.Check
		main_category: DF.Link | None
		naming_series: DF.Literal["CNCL-TA-.{topic}.##"]
		parent_assignment: DF.Link | None
		status: DF.Literal["", "Pending Review", "Pending Acceptance", "Accepted", "Rejected"]
		sub_category: DF.Link | None
		title: DF.Data
		topic: DF.Link | None
	# end: auto-generated types
	def validate(self):
		self.validate_main_sub_category_relationship()
	def autoname(self):
		if (self.topic and  not self.is_group):
			# When there is a specific topic linked, include it in the name
			self.name = frappe.model.naming.make_autoname(f'CNCL-TA-.{self.topic}.-.###')
		else:	
			# For grouped assignments without a specific topic
			self.name = frappe.model.naming.make_autoname('CNCL-TA-GRP-.YY.-.MM.-.####')

	def before_save(self):
		if self.is_group:
			# Iterate over grouped assignments and set the Parent field
			for assignment in self.grouped_assignments:
				frappe.db.set_value('Topic Assignment', assignment.topic_assignment, 'parent_assignment', self.name)
		else:
				if (self.parent_assignment):
					parent_doc = frappe.get_doc('Topic Assignment', self.parent_assignment)
					parent_doc.append('grouped_assignments', {
						'topic_assignment': self.name,
						'title': self.title,
						'assignment_date': self.assignment_date
					})
					parent_doc.save(ignore_permissions=True)


  
	def validate_main_sub_category_relationship(self):
		"""
		Validate the relationship between main category and sub-category, and check that the selected sub category is one of the  selected main category's sub categories
		"""
		if(self.main_category and self.sub_category):
			main_category_of_selected_sub=frappe.get_value("Topic Sub Category",self.sub_category,"main_category")
			# Check if the main category of the sub-category does not  match the selected main category
			if main_category_of_selected_sub!=self.main_category:
				frappe.throw(
					_("{0} is not sub category of {1}").format(self.sub_category,self.main_category)
				)
		
		
# Assuming your app structure supports this placement




@frappe.whitelist()
def get_available_topics(doctype, txt, searchfield, start, page_len, filters):
    # Ensure that 'council' is provided in filters
    # if not filters or 'council' not in filters:
    #     frappe.throw(_("Filters must contain 'council'."))

    return frappe.db.sql(
        """SELECT name FROM `tabTopic`
        WHERE docstatus= %(docstatus)s  AND 
        council = %(council)s AND 
        status IN %(status)s AND
        name NOT IN (
            SELECT topic
            FROM `tabTopic Assignment`
            WHERE council = %(council)s
        )
        ORDER BY name
       """,
        {
            "council": filters.get("council"),
            "docstatus":filters.get("docstatus"),
            "status":filters.get("status")
            
        },
        as_list=True
    )

