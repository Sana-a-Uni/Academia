# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
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
	

	@frappe.whitelist()
	def get_linked_council(self,docname):
		# Check if the 'Council' document with the given docname exists in the database
		if frappe.db.exists('Council', docname):
			# Retrieve and return the 'Council' document as a Frappe document object
			return frappe.get_doc('Council', docname)

	@frappe.whitelist()
	def get_assignments(self,council):
		"""Retrieves a list of Topic Assignment records that meet specific criteria.

		This function is accessible via a REST API endpoint due to the @frappe.whitelist() decorator.

		Args:
			council (str): The name of the council for which to retrieve assignments.

		Returns:
			list: A list of Topic Assignment records matching the filters.

		Filters:
			- docstatus: 0 (not submitted)
			- council: The provided council name
			- status: "Accepted"
		"""
		topic_assignments = frappe.get_all("Topic Assignment",fields=["*"],filters={'docstatus': 0,"council":council,"status":"Accepted"})
		return topic_assignments

	def create_new_assignment(self,title: str,description:str,date,council,topic):
		"""Creates a new Topic Assignment record with the specified details.

		Args:
			title (str): The title of the assignment.
			description (str): The description of the assignment.
			date (date): The assignment date.
			council (str): The name of the council associated with the assignment.
			topic (str): The name of the topic associated with the assignment.

		Returns:
			Document: The newly created Topic Assignment document.
		"""
		doc_assignment = frappe.new_doc("Topic Assignment")
		doc_assignment.title=title
		doc_assignment.description=description
		doc_assignment.assignment_date=date
		doc_assignment.council=council
		doc_assignment.topic=topic
		doc_assignment.status="Accepted"
		doc_assignment.insert()
		return doc_assignment
   
	# This function handles actions to be performed when the document is submitted.
	def on_submit(self):
		# Retrieve session assignments from the document
		session_assignments = self.assignments

		# Process each session assignment
		for session_assignment in session_assignments:
			# Retrieve details of the corresponding Topic Assignment
			session_assignment_doc = frappe.get_value("Topic Assignment", session_assignment.topic_assignment, ["*"], as_dict=1)

			# If the decision type is "Postponed":
			if session_assignment.decision_type == "Postponed":
				# Create a new assignment for postponed topics
				if session_assignment_doc:
					doc_assignment = self.create_new_assignment(
						title=session_assignment_doc.title,
						description=session_assignment_doc.description,
						date=frappe.utils.nowdate(),
						council=self.council,
						topic=session_assignment_doc.topic
					)
					session_assignment.forward_assignment = doc_assignment.name  # Link the new assignment

			# Update the Topic Assignment with the decision details
			session_assignment_doc.decision = session_assignment.decision
			frappe.db.set_value('Topic Assignment', session_assignment_doc.name, {
				'decision': session_assignment.decision,
				'docstatus': 1,  # Mark as submitted
				'decision_type': session_assignment.decision_type
			})