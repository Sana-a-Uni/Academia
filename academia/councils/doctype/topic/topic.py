# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import json

import frappe
from frappe import _
from frappe.model.document import Document


class Topic(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.councils.doctype.topic_attachment.topic_attachment import TopicAttachment
		from frappe.types import DF

		amended_from: DF.Link | None
		assignment_date: DF.Date
		attachments: DF.Table[TopicAttachment]
		category: DF.Link
		council: DF.Link
		decision: DF.TextEditor | None
		decision_type: DF.Literal["", "Postponed", "Resolved", "Transferred"]
		description: DF.TextEditor
		is_group: DF.Check
		parent_assignment: DF.Link | None
		status: DF.Literal["Accepted", "Pending Review", "Pending Acceptance", "Rejected"]
		title: DF.Data

	# end: auto-generated types
	def validate(self):
		if not self.get("__islocal") and self.is_group:
			self.validate_grouped_assignments()
		self.validate_parent_assignment()
		# self.ckeck_main_and_sub_categories()
		# self.validate_main_sub_category_relationship()

	def autoname(self):
		if not self.is_group:
			# When there is a specific topic linked, include it in the name
			self.name = frappe.model.naming.make_autoname(f"CNCL-TA-.YY.-.MM.-.{self.council}.-.###")
		else:
			# For grouped assignments without a specific topic
			self.name = frappe.model.naming.make_autoname(f"CNCL-TA-GRP-.YY.-.MM.-.{self.council}.-.###")

	def on_submit(self):
		if self.is_group:
			self.submit_grouped_assignments()

	# def validate_main_sub_category_relationship(self):
	# 	"""
	# 	Validate the relationship between main category and sub-category, and check that the selected sub category is one of the  selected main category's sub categories
	# 	"""
	# 	if self.main_category and self.sub_category:
	# 		main_category_of_selected_sub = frappe.get_value(
	# 			"Topic Sub Category", self.sub_category, "main_category"
	# 		)
	# 		# Check if the main category of the sub-category does not  match the selected main category
	# 		if main_category_of_selected_sub != self.main_category:
	# 			frappe.throw(
	# 				_("{0} is not sub category of {1}").format(self.sub_category, self.main_category)
	# 			)

	def submit_grouped_assignments(self):
		if self.decision_type in ["Resolved", "Transferred"]:
			grouped_assignments = frappe.get_all(
				"Topic Assignment", filters={"parent_assignment": self.name, "is_group": 0}, fields=["name"]
			)
			if len(grouped_assignments) > 0:
				for assignment_data in grouped_assignments:
					assignment = frappe.get_doc("Topic Assignment", assignment_data["name"])
					assignment.decision_type = self.decision_type
					assignment.decision = self.decision
					assignment.flags.ignore_validate = True
					assignment.save(ignore_permissions=True)
					assignment.submit()

	def validate_parent_assignment(self):
		"""
		Validates the parent assignment of the current Topic Assignment.

		Ensures that:
		1. The parent assignment is a group assignment.
		2. The parent assignment's council matches the current assignment's council.
		3. The parent assignment is not submitted or canceled.
		"""
		if self.parent_assignment:
			parent_assignment = frappe.db.get_value(
				"Topic Assignment", self.parent_assignment, ["council", "is_group", "docstatus"], as_dict=1
			)
			if parent_assignment["is_group"] == 1:  # is group
				if parent_assignment["council"] != self.council:
					frappe.throw(
						_(
							"The council of the parent assignment does not match the current assignment's council."
						)
					)
				if parent_assignment["docstatus"] != 0:
					status = "submitted" if parent_assignment["docstatus"] == 1 else "canceled"
					frappe.throw(
						_(f"The chosen parent assignment {self.parent_assignment} cannot be {status}.")
					)
			else:
				frappe.throw(_("The chosen parent assignment is not a group assignment."))

	# def ckeck_main_and_sub_categories(self):
	# 	"""
	# 	Validates that both main_category and sub_category fields are set.
	# 	Throws an error if any of these fields are missing.
	# 	"""
	# 	if not self.main_category:
	# 		frappe.throw(_("Main category must be set."))
	# 	elif not self.sub_category:
	# 		frappe.throw(_("Sub category must be set."))

	def validate_grouped_assignments(self):
		"""
		Validates that all grouped Topic Assignments have the same council
		as the current group Topic Assignment and are not group assignments.
		"""
		grouped_assignments = frappe.get_all(
			"Topic Assignment",
			filters={"parent_assignment": self.name},
			fields=["name", "council", "is_group"],
		)

		for assignment in grouped_assignments:
			if assignment.council != self.council:
				frappe.throw(
					_(
						"Grouped topic assignment {0} does not have the same council as the group assignment."
					).format(assignment.name)
				)
			if assignment.is_group:
				frappe.throw(
					_("Grouped topic assignment {0} can not be of type group.").format(assignment.name)
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
			"docstatus": filters.get("docstatus"),
			"status": filters.get("status"),
		},
		as_list=True,
	)


@frappe.whitelist()
def get_grouped_assignments(parent_name):
	grouped_assignments = frappe.get_all(
		"Topic Assignment",
		filters={"parent_assignment": parent_name, "is_group": 0},
		fields=["name", "title", "assignment_date", "decision_type"],
	)
	return grouped_assignments


@frappe.whitelist()
def add_assignments_to_group(parent_name, assignments):
	try:
		assignments_list = json.loads(assignments)  # Parse the JSON string into a list
		for assignment_name in assignments_list:
			assignment = frappe.get_doc("Topic Assignment", assignment_name)
			assignment.parent_assignment = parent_name
			assignment.save()

		return "ok"
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Error adding assignments")
		return str(e)


@frappe.whitelist()
@frappe.whitelist()
def delete_assignments_from_group(assignment_names):
	try:
		assignments_list = json.loads(assignment_names)  # Parse the JSON string into a list
		for assignment_name in assignments_list:
			assignment = frappe.get_doc("Topic Assignment", assignment_name)
			assignment.parent_assignment = None
			assignment.save()

		return "ok"
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Error removing assignments")
		return str(e)
