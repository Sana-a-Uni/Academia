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

        approval_date: DF.Date | None
        course_language: DF.TableMultiSelect[CourseLanguage]
        courses: DF.Check
        date_of_programe_development: DF.Date
        delivery_mode: DF.Literal["", "On Campus", "Online"]
        effective_year: DF.Link | None
        faculty: DF.Link
        faculty_department: DF.Link
        file: DF.Attach | None
        maximum_research_period: DF.Int
        minimum_course_average_to_start_research: DF.Data | None
        minimum_research_period: DF.Int
        program_abbreviation: DF.Data
        program_degree: DF.Data
        program_name: DF.Link
        research_or_thesis: DF.Check
        starrting_year_of_the_program: DF.Date | None
        study_methods: DF.Link | None
        table_ytno: DF.Table[StudyPlanCourse]
        total_hours_required_to_award_degree: DF.Int
    # end: auto-generated types
    pass
