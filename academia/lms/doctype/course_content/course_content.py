# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CourseContent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.lms.doctype.attachment_files.attachment_files import AttachmentFiles
		from frappe.types import DF

		attachment_files: DF.Table[AttachmentFiles]
		course: DF.Link | None
		course_type: DF.Link | None
		faculty_member: DF.Link | None
		title: DF.Data | None
		topic: DF.TextEditor | None
	# end: auto-generated types
	pass
