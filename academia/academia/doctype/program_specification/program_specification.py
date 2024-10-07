# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProgramSpecification(Document):
    def get_course_list(self):
        return [frappe.get_doc("Course Specification", study_plan_course.course_code) for study_plan_course in self.table_ytno]

    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.academia.doctype.course_language.course_language import CourseLanguage
        from academia.academia.doctype.study_plan_course.study_plan_course import StudyPlanCourse
        from frappe.types import DF

        abbr: DF.ReadOnly
        academic_degree: DF.ReadOnly
        academic_system: DF.Literal["", "Semester System", "Credit Hours System"]
        approval_date: DF.Date | None
        course_language: DF.TableMultiSelect[CourseLanguage]
        courses: DF.Check
        date_of_programe_development: DF.Date
        date_of_starting_the_program: DF.Date | None
        delivery_mode: DF.Literal["", "On Campus", "Online"]
        faculty: DF.ReadOnly
        faculty_department: DF.ReadOnly
        file: DF.Attach | None
        implementation_start_academic_year: DF.Link | None
        maximum_research_period: DF.Int
        minimum_course_average_to_start_research: DF.Data | None
        minimum_research_period: DF.Int
        program_name: DF.Link
        program_name_english: DF.ReadOnly
        research_or_thesis: DF.Check
        table_ytno: DF.Table[StudyPlanCourse]
        total_hours_required_to_award_degree: DF.Int
    # end: auto-generated types
    pass
