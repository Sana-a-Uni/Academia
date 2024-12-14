# Copyright (c) 2023, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Student(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.place_of_birth.place_of_birth import PlaceofBirth
		from academia.academia.doctype.student_guardian.student_guardian import StudentGuardian
		from frappe.types import DF

		academic_level: DF.Link | None
		academic_status: DF.Link | None
		blood_group: DF.Literal["", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
		city: DF.Data | None
		county: DF.Data | None
		current_department: DF.Data | None
		current_faculty: DF.Data | None
		current_student_batch: DF.Data | None
		current_student_id: DF.Data | None
		current_student_level: DF.Data | None
		current_student_program: DF.Data | None
		date_of_birth: DF.Date | None
		date_of_leaving: DF.Date | None
		educational_system: DF.Literal["", "\u0627\u0644\u0646\u0638\u0627\u0645 \u0627\u0644\u0639\u0627\u0645", "\u0627\u0644\u0646\u0638\u0627\u0645 \u0627\u0644\u0645\u0648\u0627\u0632\u064a", "\u0646\u0641\u0642\u0629 \u062e\u0627\u0635\u0629"]
		first_name: DF.Data
		first_name_en: DF.Data | None
		gender: DF.Literal["", "Male", "Female"]
		guardians: DF.Table[StudentGuardian]
		high_school_year: DF.Data | None
		identification_number: DF.Data | None
		image: DF.AttachImage | None
		joining_date: DF.Date | None
		last_name: DF.Data | None
		last_name_en: DF.Data | None
		leaving_certificate_number: DF.Data | None
		middle_name: DF.Data | None
		middle_name_en: DF.Data | None
		mobile_number: DF.Phone | None
		naming_series: DF.Literal["EDU-STU-.YYYY.-"]
		nationality: DF.Data | None
		personal_email: DF.Data | None
		place_of_birth: DF.Table[PlaceofBirth]
		reason_for_leaving: DF.Text | None
		secondary_degree: DF.Data | None
		secondary_directorate: DF.Data | None
		secondary_governorate: DF.Data | None
		secondary_rate: DF.Data | None
		secondary_type: DF.Literal["", "\u0639\u0644\u0645\u064a", "\u0627\u062f\u0628\u064a"]
		sitting_number: DF.Data | None
		state: DF.Link | None
		student_applicant: DF.Link | None
		student_mobile_number: DF.Phone | None
		student_name: DF.Data | None
		title: DF.Check
		university_email: DF.Data | None
		user_id: DF.Link | None
	# end: auto-generated types
	pass
