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
		from academia.councils.doctype.topic_attachment.topic_attachment import TopicAttachment
		from frappe.types import DF

		amended_from: DF.Link | None
		assignment_date: DF.Date
		attachments: DF.Table[TopicAttachment]
		council: DF.Link
		decision: DF.TextEditor | None
		decision_type: DF.Literal["", "Postponed", "Resolved", "Transferred"]
		description: DF.TextEditor
		is_group: DF.Check
		main_category: DF.Link | None
		parent_assignment: DF.Link | None
		status: DF.Literal["Accepted", "Pending Review", "Pending Acceptance", "Rejected"]
		sub_category: DF.Link | None
		title: DF.Data
		topic: DF.Link | None
	# end: auto-generated types
	def validate(self):
		# self.validate_grouped_assignments()
		self.validate_main_sub_category_relationship()
	def autoname(self):
		if (not self.is_group):
			# When there is a specific topic linked, include it in the name
			self.name = frappe.model.naming.make_autoname(f'CNCL-TA-.YY.-.MM.-.{self.council}.-.###')
		else:
			# For grouped assignments without a specific topic
			self.name = frappe.model.naming.make_autoname(f'CNCL-TA-GRP-.YY.-.MM.-.{self.council}.-.###')


	def validate_grouped_assignments(self):

		if not self.is_group:
			self.grouped_assignments = []
			return
		self.parent_assignment = None
		# Check if grouped assignments are required but not provided
		if not self.grouped_assignments:
			frappe.throw("Grouped Assignments are required if 'Is Group' is checked.")
		unique_assignments = []
		topic_assignment_set = set()
		for assignment in self.grouped_assignments:
			# Fetch the related Topic Assignment document
			if assignment.topic_assignment not in topic_assignment_set:
				topic_assignment_set.add(assignment.topic_assignment)
				unique_assignments.append(assignment)
			topic_assignment = frappe.get_doc("Topic Assignment", assignment.topic_assignment)
			if topic_assignment.council != self.council:
				frappe.throw(f"Assignment {topic_assignment.title} does not belong to the {self.council} council.")
		self.grouped_assignments = unique_assignments

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




@frappe.whitelist()
def get_available_topics(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        """SELECT name FROM `tabTopic`
        WHERE docstatus= %(docstatus)s  AND
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


@frappe.whitelist()
def get_grouped_assignments(parent_name):
	query = """
		-- Fetch direct assignments linked to the topic
		SELECT
			ta.name ,
			ta.title ,
			ta.assignment_date ,
			ta.decision_type
		FROM
			`tabTopic Assignment` ta
		WHERE
			ta.parent_assignment = %s
		ORDER BY assignment_date
	"""
	data = frappe.db.sql(query, (parent_name), as_dict=True)
	return data


@frappe.whitelist()
def add_assignment_to_group(parent_name, assignment_name):
	try:
		frappe.db.set_value('Topic Assignment', assignment_name, 'parent_assignment', parent_name)
		return "ok"
	except Exception as e:
		frappe.log_error(message=str(e))
		return str(e)


@frappe.whitelist()
def delete_assignment_from_group(assignment_name):
	try:
		frappe.db.set_value('Topic Assignment', assignment_name, 'parent_assignment', None)
		return "ok"
	except Exception as e:
		frappe.log_error(message=str(e))
		return str(e)