# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AssignmentSubmission(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.lms.doctype.attachment_files.attachment_files import AttachmentFiles
		from frappe.types import DF

		amended_from: DF.Link | None
		answer: DF.TextEditor | None
		assignment: DF.Link | None
		attachment_files: DF.Table[AttachmentFiles]
		comment: DF.TextEditor | None
		student: DF.Link | None
		submission_date: DF.Datetime | None
	# end: auto-generated types
	pass
