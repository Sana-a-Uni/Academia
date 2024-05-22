# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import json

class Topic(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.councils.doctype.topic_applicant.topic_applicant import TopicApplicant
		from frappe.types import DF

		amended_from: DF.Link | None
		applicants: DF.Table[TopicApplicant]
		application_date: DF.Datetime
		council: DF.Link
		description: DF.TextEditor
		related_to: DF.Link | None
		status: DF.Literal["Open", "Complete", "in Progress", "Hold", "Closed"]
		title: DF.Data 
		topic_main_category: DF.Link
		topic_sub_category: DF.Link
	# end: auto-generated types
	def onload(self):
		if self.has_topic_assignment():
			self.set_onload('has_topic_assignment', True)
		else:
			self.set_onload('has_topic_assignment', False)
		
	def validate(self):
		self.validate_main_sub_category_relationship()
		self.check_for_duplicate_applicants()

	def validate_main_sub_category_relationship(self):
		"""
		Validate the relationship between main category and sub-category, and check that the selected sub category is one of the  selected main category's sub categories
		"""
		if(self.topic_main_category and self.topic_sub_category):
			main_category_of_selected_sub=frappe.get_value("Topic Sub Category",self.topic_sub_category,"main_category")
			# Check if the main category of the sub-category does not  match the selected main category
			if main_category_of_selected_sub!=self.topic_main_category:
				frappe.throw(
					_("{0} is not sub category of {1}").format(self.topic_sub_category,self.topic_main_category)
				)
		
		
	def check_for_duplicate_applicants(self):
		"""
		Ensures no duplicates in 'applicants' child table based on 'applicant' and 'applicant_type'.
		Raises ValidationError if duplicates are found.
		"""
		applicants = self.get('applicants') or []  # Ensure it's always a list
		seen_applicants = set()
		for d in applicants:
			applicant_id = (d.applicant, d.applicant_type)  # Tuple as unique identifier
			if applicant_id in seen_applicants:
				frappe.throw(f'Duplicate entry for Applicant: {d.applicant} of Type: {d.applicant_type}',
							title='Duplicate Applicant Error')
			seen_applicants.add(applicant_id)		
			
	def has_topic_assignment(self):
		"""
		Check if the topic has been assigned to a council
		"""
		assignments = frappe.get_all('Topic Assignment', 
                                 filters={'topic': self.name}, 
                                 fields=['name'])
		if assignments:
			return True



@frappe.whitelist()
def get_all_related_assignments(topic_name):
	query = """
		-- Fetch direct assignments linked to the topic
		SELECT
			ta.name ,
			ta.title ,
			ta.status ,
			ta.council ,
			ta.assignment_date ,
			ta.decision_type ,
			ta.parent_assignment 
		FROM
			`tabTopic Assignment` ta
		WHERE
			ta.topic = %s

		UNION

		-- Fetch parent assignments where any child assignment is linked to the topic
		SELECT
			parent_ta.name,
			parent_ta.title,
			parent_ta.status,
			parent_ta.council,
			parent_ta.assignment_date,
			parent_ta.decision_type,
			parent_ta.parent_assignment
		FROM
			`tabTopic Assignment` AS child_ta
		INNER JOIN
			`tabTopic Assignment` AS parent_ta ON child_ta.parent_assignment = parent_ta.name
		WHERE
			child_ta.topic = %s AND
			child_ta.parent_assignment IS NOT NULL

		ORDER BY assignment_date
	"""
	data = frappe.db.sql(query, (topic_name, topic_name), as_dict=True)
	return data

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
