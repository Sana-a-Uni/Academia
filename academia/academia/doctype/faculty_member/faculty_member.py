import frappe
from frappe.model.document import Document
from frappe import _
import re
from datetime import datetime
from frappe.utils import add_months, nowdate
import logging


class FacultyMember(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.academia.doctype.faculty_member_academic_ranking.faculty_member_academic_ranking import FacultyMemberAcademicRanking
        from academia.academia.doctype.faculty_member_academic_services.faculty_member_academic_services import FacultyMemberAcademicServices
        from academia.academia.doctype.faculty_member_activity.faculty_member_activity import FacultyMemberActivity
        from academia.academia.doctype.faculty_member_award_and_appreciation_certificate.faculty_member_award_and_appreciation_certificate import FacultyMemberAwardandAppreciationCertificate
        from academia.academia.doctype.faculty_member_conference_and_workshop.faculty_member_conference_and_workshop import FacultyMemberConferenceandWorkshop
        from academia.academia.doctype.faculty_member_course.faculty_member_course import FacultyMemberCourse
        from academia.academia.doctype.faculty_member_language.faculty_member_language import FacultyMemberLanguage
        from academia.academia.doctype.faculty_member_training_course.faculty_member_training_course import FacultyMemberTrainingCourse
        from academia.academia.doctype.faculty_member_university_and_community_service.faculty_member_university_and_community_service import FacultyMemberUniversityandCommunityService
        from frappe.types import DF

        academic_rank: DF.Link
        academic_services: DF.TableMultiSelect[FacultyMemberAcademicServices]
        commencement_of_work_attachment: DF.Attach | None
        commencement_of_work_date: DF.Date | None
        commencement_of_work_decision_number: DF.Data | None
        company: DF.Link
        courses: DF.TableMultiSelect[FacultyMemberCourse]
        date: DF.Date | None
        date_of_joining_in_service: DF.Date | None
        date_of_joining_in_university: DF.Date | None
        date_of_obtaining_the_academic_rank: DF.Date | None
        decision_attachment: DF.Attach | None
        decision_number: DF.Data | None
        department: DF.Link
        email: DF.Data
        employee: DF.Link
        employment_type: DF.Link | None
        external_faculty: DF.Link | None
        faculty: DF.Link
        faculty_member_academic_ranking: DF.Table[FacultyMemberAcademicRanking]
        faculty_member_activity: DF.Table[FacultyMemberActivity]
        faculty_member_award_and_appreciation_certificate: DF.Table[FacultyMemberAwardandAppreciationCertificate]
        faculty_member_conference_and_workshop: DF.Table[FacultyMemberConferenceandWorkshop]
        faculty_member_name: DF.Data
        faculty_member_name_english: DF.Data | None
        faculty_member_training_course: DF.Table[FacultyMemberTrainingCourse]
        faculty_member_university_and_community_service: DF.Table[FacultyMemberUniversityandCommunityService]
        from_another_university: DF.Link | None
        general_field: DF.Data | None
        google_scholar_profile_link: DF.Data | None
        image: DF.AttachImage | None
        is_eligible_for_granting_tenure: DF.Check
        languages: DF.TableMultiSelect[FacultyMemberLanguage]
        naming_series: DF.Literal["ACAD-FM-"]
        nationality: DF.Link | None
        probation_period_end_date: DF.Date | None
        scientific_degree: DF.Link
        specialist_field: DF.Data | None
        tenure_status: DF.Literal["", "On Probation", "Tenured"]
    # end: auto-generated types
    # Begin auto-generated types

    def validate(self):
        # Calling functions
        self.validate_duplicate_employee()
        self.validate_date()
        self.validate_url()
        self.validate_decision_number()
        self.get_probation_end_date()
        self.check_tenure_eligibility()
    # End of validate controller hook

    # Validate duplicate 'employee' field
    def validate_duplicate_employee(self):
        if self.employee:
            exist_employee = frappe.get_value("Faculty Member", {"employee": self.employee, "name": ["!=", self.name]}, "faculty_member_name")
            if exist_employee:
                frappe.throw(_(f"Employee {self.employee} is already assigned to {exist_employee}"))

    # Validate 'date_of_joining_in_university' and 'date_of_joining_in_service' and 'date in tenure data' fields
    def validate_date(self):
        today = frappe.utils.today()
        
        if self.date_of_joining_in_service:
            if self.date_of_joining_in_service > today:
                frappe.throw(_("Date of joining in service cannot be in the future."))
        
        if self.date_of_joining_in_university:
            if self.date_of_joining_in_university > today:
                frappe.throw(_("Date of joining in university cannot be in the future."))
        
        if self.date_of_joining_in_service and self.date_of_joining_in_university:
            if self.date_of_joining_in_service > self.date_of_joining_in_university:
                frappe.throw(_("Date of joining in service must be before the date of joining in university."))

        if self.date:
            if self.date > today:
                frappe.throw(_("Date in tenure data section cannot be in the future."))

    # Validate 'google_scholar_profile_link' field
    def validate_url(self):
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        if self.google_scholar_profile_link:
            if not url_pattern.match(self.google_scholar_profile_link):
                frappe.throw(_("Google Scholar Profile Link is not valid. Please enter a valid URL starting with http, https, or ftp."))

    # Validate 'decision_number' field
    def validate_decision_number(self):
        if self.decision_number and not self.decision_number.isdigit():
            frappe.throw(_("Decision Number should contain only digits."))

    # Fetch and set probation end date
    def get_probation_end_date(self):
        if self.commencement_of_work_date and self.tenure_status == "On Probation" and self.employment_type == "Official":
            faculty_member_settings = frappe.get_all(
                "Faculty Member Settings",
                filters=[
                    ["academic_rank", "=", self.academic_rank],
                    ["valid_from", "<=", self.commencement_of_work_date],
                ],
                fields=["name", "probation_period"],
                order_by="valid_from desc",
            )
            
            if faculty_member_settings:
                faculty_member_settings = faculty_member_settings[0]
                self.probation_period_end_date = add_months(
                    self.commencement_of_work_date,
                    int(faculty_member_settings.probation_period),
                )
            else:
                frappe.throw(
                    _(
                        "Probation periods not found in Faculty Member Settings for <b>{}</b> from this date. Please create appropriate settings.".format(self.academic_rank)
                    ),
                    title=_("Missing Probation Settings"),
                )

    # Check tenure eligibility
    def check_tenure_eligibility(self):
        if self.probation_period_end_date:
            try:
                probation_end_date = datetime.strptime(self.probation_period_end_date, "%Y-%m-%d").date()
                today = datetime.strptime(nowdate(), "%Y-%m-%d").date()

                if probation_end_date >= today:
                    self.is_eligible_for_granting_tenure = 1
                else:
                    self.is_eligible_for_granting_tenure = 0

            except ValueError as e:
                frappe.msgprint(_("Error parsing probation end date: {0}").format(e), title=_("Date Parsing Error"), indicator="red")
                self.is_eligible_for_granting_tenure = 0
