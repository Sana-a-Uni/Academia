# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


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
 
	def validate(self):
		self.validate_main_sub_category_relationship()
		self.check_duplicate_applicant()

	def validate_main_sub_category_relationship(self):
		"""
		Validate the relationship between main category and sub-category, and check that the selected sub category is one of the  selected main category's sub categories
		"""
		main_category_of_selected_sub=frappe.get_value("Topic Sub Category",self.topic_sub_category,"topic_main_category")
		# Check if the main category of the sub-category does not  match the selected main category
		if main_category_of_selected_sub!=self.topic_main_category:
			frappe.throw(
				_("{0} is not sub category of {1}").format(self.topic_sub_category,self.topic_main_category)
			)
		
	def check_duplicate_applicant(self):
		"""check for duplicate topic applicant"""
		found=[]
		for applicant in self.applicants:
			# Get the value of user field of the applicant
			user= get_applicant_user(applicant_type= applicant.applicant_type, applicant=applicant.applicant)
			# Check if the user is already in the found list
			if user in found:
				frappe.throw(
        			_("Applicant {0} entered before ").format(applicant.applicant_name)
           					)
			found.append(user)   

@frappe.whitelist()
def get_applicant_user(applicant_type,applicant):
    """
	Retrieve the user associated with the applicant.
	Args:
		applicant_type (str): The document type(Doctype) .
		applicant (str): The document name.
	Returns:
		str: The value of the user field of the applicant.
	"""
    user=frappe.get_value(applicant_type, applicant, "user")
    return user
