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
		from academia.councils.doctype.topic_applicant.topic_applicant import TopicApplicant
		from academia.councils.doctype.topic_attachment.topic_attachment import TopicAttachment
		from frappe.types import DF

		amended_from: DF.Link | None
		applicants: DF.Table[TopicApplicant]
		attachments: DF.Table[TopicAttachment]
		category: DF.Link
		council: DF.Link
		decision: DF.TextEditor | None
		decision_type: DF.Literal["", "Postponed", "Resolved"]
		description: DF.TextEditor
		is_group: DF.Check
		parent_topic: DF.Link | None
		status: DF.Literal["Accepted", "Pending Review", "Pending Acceptance", "Rejected"]
		title: DF.Data
		topic_date: DF.Date
		transaction: DF.Link
		transaction_action: DF.Link

	# end: auto-generated types
	def validate(self):
		if not self.get("__islocal") and self.is_group:
			self.validate_grouped_topics()
		self.validate_parent_topic()
		# self.check_main_and_sub_categories()
		# self.validate_main_sub_category_relationship()

	def autoname(self):
		if not self.is_group:
			# When there is a specific topic linked, include it in the name
			self.name = frappe.model.naming.make_autoname(f"CNCL-TPC-.YY.-.MM.-.{self.council}.-.###")
		else:
			# For grouped topics without a specific topic
			self.name = frappe.model.naming.make_autoname(f"CNCL-TPC-GRP-.YY.-.MM.-.{self.council}.-.###")

	def on_submit(self):
		if self.is_group:
			self.submit_grouped_topics()

	# def validate_main_sub_category_relationship(self):
	#     """
	#     Validate the relationship between main category and sub-category, and check that the selected sub category is one of the  selected main category's sub categories
	#     """
	#     if self.main_category and self.sub_category:
	#         main_category_of_selected_sub = frappe.get_value(
	#             "Topic Sub Category", self.sub_category, "main_category"
	#         )
	#         # Check if the main category of the sub-category does not  match the selected main category
	#         if main_category_of_selected_sub != self.main_category:
	#             frappe.throw(
	#                 _("{0} is not sub category of {1}").format(self.sub_category, self.main_category)
	#             )

	def submit_grouped_topics(self):
		if self.decision_type in ["Resolved", "Transferred"]:
			grouped_topics = frappe.get_all(
				"Topic", filters={"parent_topic": self.name, "is_group": 0}, fields=["name"]
			)
			if len(grouped_topics) > 0:
				for topic_data in grouped_topics:
					topic = frappe.get_doc("Topic", topic_data["name"])
					topic.decision_type = self.decision_type
					topic.decision = self.decision
					topic.flags.ignore_validate = True
					topic.save(ignore_permissions=True)
					topic.submit()

	def validate_parent_topic(self):
		"""
		Validates the parent topic of the current Topic.

		Ensures that:
		1. The parent topic is a group topic.
		2. The parent topic's council matches the current topic's council.
		3. The parent topic is not submitted or canceled.
		"""
		if self.parent_topic:
			parent_topic = frappe.db.get_value(
				"Topic", self.parent_topic, ["council", "is_group", "docstatus"], as_dict=1
			)
			if parent_topic["is_group"] == 1:  # is group
				if parent_topic["council"] != self.council:
					frappe.throw(
						_("The council of the parent topic does not match the current topic's council.")
					)
				if parent_topic["docstatus"] != 0:
					status = "submitted" if parent_topic["docstatus"] == 1 else "canceled"
					frappe.throw(_(f"The chosen parent topic {self.parent_topic} cannot be {status}."))
			else:
				frappe.throw(_("The chosen parent topic is not a group topic."))

	# def check_main_and_sub_categories(self):
	#     """
	#     Validates that both main_category and sub_category fields are set.
	#     Throws an error if any of these fields are missing.
	#     """
	#     if not self.main_category:
	#         frappe.throw(_("Main category must be set."))
	#     elif not self.sub_category:
	#         frappe.throw(_("Sub category must be set."))

	def validate_grouped_topics(self):
		"""
		Validates that all grouped Topics have the same council
		as the current group Topic and are not group topics.
		"""
		grouped_topics = frappe.get_all(
			"Topic",
			filters={"parent_topic": self.name},
			fields=["name", "council", "is_group"],
		)

		for topic in grouped_topics:
			if topic.council != self.council:
				frappe.throw(
					_("Grouped topic {0} does not have the same council as the group topic.").format(
						topic.name
					)
				)
			if topic.is_group:
				frappe.throw(_("Grouped topic {0} can not be of type group.").format(topic.name))


# @frappe.whitelist()
# def get_available_topics(doctype, txt, searchfield, start, page_len, filters):
# 	return frappe.db.sql(
# 		"""SELECT name FROM `tabTopic`
#         WHERE docstatus= %(docstatus)s  AND
#         status IN %(status)s AND
#         name NOT IN (
#             SELECT topic
#             FROM `tabTopic`
#             WHERE council = %(council)s
#         )
#         ORDER BY name
#        """,
# 		{
# 			"council": filters.get("council"),
# 			"docstatus": filters.get("docstatus"),
# 			"status": filters.get("status"),
# 		},
# 		as_list=True,
# 	)


@frappe.whitelist()
def get_grouped_topics(parent_name):
	grouped_topics = frappe.get_all(
		"Topic",
		filters={"parent_topic": parent_name, "is_group": 0},
		fields=["name", "title", "topic_date", "decision_type"],
	)
	return grouped_topics


@frappe.whitelist()
def add_topics_to_group(parent_name, topics):
	try:
		topics_list = json.loads(topics)  # Parse the JSON string into a list
		for topic_name in topics_list:
			topic = frappe.get_doc("Topic", topic_name)
			topic.parent_topic = parent_name
			topic.save()

		return "ok"
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Error adding topics")
		return str(e)


@frappe.whitelist()
def delete_topics_from_group(topic_names):
	try:
		topics_list = json.loads(topic_names)  # Parse the JSON string into a list
		for topic_name in topics_list:
			topic = frappe.get_doc("Topic", topic_name)
			topic.parent_topic = None
			topic.save()

		return "ok"
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Error removing topics")
		return str(e)


from frappe.model.mapper import get_mapped_doc
from frappe.utils import today


@frappe.whitelist()
def create_topic_from_transaction(transaction_name, transaction_action, target_doc=None):
	def set_additional_values(source_doc, target_doc, source_parent_doc):
		target_doc.topic_date = today()
		target_doc.transaction = transaction_name
		target_doc.transaction_action = transaction_action
		target_doc.council = get_council_for_topic()

	def get_council_for_topic():
		user = frappe.session.user  # Get the current logged in user
		employee = frappe.db.get_value("Employee", {"user_id": user}, "name")  # Fetch the linked employee

		if not employee:
			frappe.throw(_("No linked employee found for the current user."))

		# Find if the employee is a head in any council
		council = frappe.db.sql(
			"""
			SELECT * FROM `tabCouncil Member`
			WHERE employee=%s AND member_role='Council Head'
			LIMIT 1
		""",
			(employee,),
			as_dict=1,
		)
		if not council:
			frappe.throw(_("You are not listed as head of any council"))

		return council[0].parent if council else None

	# Define the mapping specifications
	mappings = {
		"Transaction": {
			"doctype": "Topic",
			"field_map": {"category": "category", "title": "title", "description": "description"},
			"postprocess": set_additional_values,
		},
		"Topic Attachment": {
			"doctype": "Topic Attachment",
			"field_map": {
				"title": "title",
				"type": "type",
				"attachment": "attachment",
				"upload_date": "upload_date",
			},
		},
		"Topic Applicant": {
			"doctype": "Topic Applicant",
			"field_map": {
				"applicant_type": "applicant_type",
				"applicant": "applicant",
				"applicant_name": "applicant_name",
			},
		},
	}

	# Create the Topic document based on the mappings from the Transaction
	topic_doc = get_mapped_doc("Transaction", transaction_name, mappings, target_doc)

	try:
		# topic_doc.flags.ignore_permissions = True     #get_mapped_doc does check create permission so we can ignore them in insert to reduce checking time
		topic_doc.insert()  # No longer ignoring permissions, ensuring enforcement
		frappe.db.commit()
	except frappe.PermissionError:
		frappe.throw(_("Not permitted"), frappe.PermissionError)

		return topic_doc.name
