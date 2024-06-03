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
		from frappe.types import DF

		from academia.councils.doctype.topic_applicant.topic_applicant import TopicApplicant
		from academia.councils.doctype.topic_attachment.topic_attachment import TopicAttachment

		amended_from: DF.Link | None
		applicants: DF.Table[TopicApplicant]
		application_date: DF.Datetime
		attachments: DF.Table[TopicAttachment]
		council: DF.Link
		description: DF.TextEditor
		related_to: DF.Link | None
		status: DF.Literal["Open", "Complete", "in Progress", "Hold", "Closed"]
		title: DF.Data
		topic_main_category: DF.Link
		topic_sub_category: DF.Link
		transaction: DF.Link | None

	# end: auto-generated types
	def onload(self):
		if self.has_topic_assignment():
			self.set_onload("has_topic_assignment", True)
		else:
			self.set_onload("has_topic_assignment", False)

	def validate(self):
		self.validate_main_sub_category_relationship()
		self.check_for_duplicate_applicants()

	def validate_main_sub_category_relationship(self):
		"""
		Validate the relationship between main category and sub-category, and check that the selected sub category is one of the  selected main category's sub categories
		"""
		if self.topic_main_category and self.topic_sub_category:
			main_category_of_selected_sub = frappe.get_value(
				"Topic Sub Category", self.topic_sub_category, "main_category"
			)
			# Check if the main category of the sub-category does not  match the selected main category
			if main_category_of_selected_sub != self.topic_main_category:
				frappe.throw(
					_("{0} is not sub category of {1}").format(
						self.topic_sub_category, self.topic_main_category
					)
				)

	def check_for_duplicate_applicants(self):
		"""
		Ensures no duplicates in 'applicants' child table based on 'applicant' and 'applicant_type'.
		Raises ValidationError if duplicates are found.
		"""
		applicants = self.get("applicants") or []  # Ensure it's always a list
		seen_applicants = set()
		for d in applicants:
			applicant_id = (d.applicant, d.applicant_type)  # Tuple as unique identifier
			if applicant_id in seen_applicants:
				frappe.throw(
					f"Duplicate entry for Applicant: {d.applicant} of Type: {d.applicant_type}",
					title="Duplicate Applicant Error",
				)
			seen_applicants.add(applicant_id)

	def has_topic_assignment(self):
		"""
		Check if the topic has been assigned to a council
		"""
		assignments = frappe.get_all("Topic Assignment", filters={"topic": self.name}, fields=["name"])
		if assignments:
			return True


@frappe.whitelist()
def get_all_related_assignments(topic_name):
	"""
	Fetches all related topic assignments for a given topic. It starts with
	assignments related to the given topic and then follows tracking the chain of
	related topic assignments by parent assignments and council memos until the chain ends or a
	resolved decision type is encountered.

	Args:
	topic_name (str): The name of the topic for which related assignments are to be fetched.

	Returns:
	list: A list of dictionaries, where each dictionary represents a topic assignment.
	"""

	# Define the fields to be retrieved for each assignment
	fields_names = [
		"name",
		"title",
		"status",
		"council",
		"assignment_date",
		"decision_type",
		"parent_assignment",
		"is_group",
	]

	# Get all assignments related to the given topic, ordered by assignment date
	assignments = frappe.db.get_all(
		"Topic Assignment", filters={"topic": topic_name}, fields=fields_names, order_by="assignment_date"
	)

	if assignments:
		# Start with the last assignment in the list
		assignment = assignments[-1]

		while True:
			# Check if the assignment has a parent assignment
			if assignment["parent_assignment"]:
				# Fetch parent assignment details
				parent_assignment = frappe.db.get_value(
					"Topic Assignment", assignment["parent_assignment"], fields_names, as_dict=1
				)

				if parent_assignment:
					# Add parent assignment to the list and update assignment
					assignments.append(parent_assignment)
					assignment = parent_assignment
				else:
					break

			# Break if the decision type is "Resolved"
			if assignment["decision_type"] == "Resolved":
				break

			# Fetch council memo related of the current assignment
			memo = frappe.db.get_value(
				"Council Memo", {"originating_assignment": assignment["name"]}, "name", as_dict=1
			)

			if memo:
				# Fetch the assignment initiated by the council memo
				related_assignment = frappe.db.get_value(
					"Topic Assignment",
					{"initiating_council_memo": memo["name"]},
					fields_names,
					as_dict=1,
				)
				if related_assignment:
					# Add related assignment to the list and update assignment
					assignments.append(related_assignment)
					assignment = related_assignment
				else:
					break
			else:
				# Break if assignment has no memo
				break

	return assignments


"""	def check_duplicate_applicant(self):
		if(self.applicants):
			found=[]
			for applicant in self.applicants:
				# Get the value of user field of the applicant
				user= frappe.get_value(applicant.applicant_type, applicant.applicant, "user_id")
				# Check if the user is already in the found list
				if user in found:
					frappe.throw(
						_("Applicant {0} entered before ").format(applicant.applicant_name)
								)
				found.append(user)

"""

# @frappe.whitelist()
# def get_applicant_users_batch(applicants):
#     """
#     Retrieve the user associated with a batch of applicants.

#     Args:
#         applicants (str): A JSON string representing a list of applicants where each applicant
#                           is a dictionary with 'applicant_type' and 'applicant' keys.

#     Returns:
#         list: A list of user values or None for each applicant in the batch.
#     """

#     try:
#         # Convert the JSON string back to a Python list of dictionaries
#         applicants_list = json.loads(applicants)
#         user_values = []

#         for applicant in applicants_list:
#             # Attempt to fetch the 'user' value for each applicant based on their type and name
#             user = frappe.get_value(applicant["applicant_type"], applicant["applicant"], "user")
#             user_values.append(user)  # Will append None if user is not found

#         return user_values
#     except Exception as e:
#         frappe.log_error(f"Error in get_applicant_users_batch: {e}", "Get Applicant Users Batch Error")
#         # Return a list of Nones to match the expected output format in case of error
#         return [None] * len(applicants_list)
