# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CourseSpecification(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.co_requisites.co_requisites import CoRequisites
		from academia.academia.doctype.course_hours.course_hours import CourseHours
		from academia.academia.doctype.course_language.course_language import CourseLanguage
		from academia.academia.doctype.pre_requisites.pre_requisites import PreRequisites
		from frappe.types import DF

		approval_date: DF.Date | None
		co_requisites: DF.TableMultiSelect[CoRequisites]
		course_code: DF.Link
		course_image: DF.AttachImage | None
		course_name: DF.Data | None
		course_name_english: DF.Data | None
		course_type: DF.ReadOnly | None
		credit_hours: DF.Table[CourseHours]
		date_of_course_development: DF.Date | None
		description: DF.TextEditor | None
		effective_academic_year: DF.Link | None
		faculty: DF.ReadOnly | None
		file: DF.Attach | None
		languages: DF.TableMultiSelect[CourseLanguage]
		pre_requisites: DF.TableMultiSelect[PreRequisites]
		program: DF.ReadOnly | None
	# end: auto-generated types
	pass
