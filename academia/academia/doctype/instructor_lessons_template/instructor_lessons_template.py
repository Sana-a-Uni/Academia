# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InstructorLessonsTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_term: DF.Link | None
		academic_year: DF.Link | None
		faculty: DF.Link | None
		instructor: DF.Link | None
		program_specification: DF.Link | None
		schedule_template_version: DF.Link | None
	# end: auto-generated types
@frappe.whitelist()
def get_lessons_data(instructor, faculty, schedule_template_version):
    """
    Fetch lessons for a specific instructor, faculty, and schedule template version.
    Returns a dictionary formatted for rendering in the timetable.
    """
    lessons = {}
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    time_slots = ["08:00 - 10:00", "10:00 - 12:00", "12:00 - 14:00", "14:00 - 16:00", "16:00 - 18:00"]

    # Initialize an empty schedule
    for day in days:
        lessons[day] = [None] * len(time_slots)  # Use None instead of empty strings

    # Mapping for time ranges
    time_mapping = {
        "8": "08:00 - 10:00",
        "10": "10:00 - 12:00",
        "12": "12:00 - 14:00",
        "14": "14:00 - 16:00",
        "16": "16:00 - 18:00"
    }

    # Fetch lessons from Lesson Template with the new filter
    lesson_templates = frappe.get_all(
        "Lesson Template",
        filters={
            "instructor": instructor,
            "faculty": faculty,
            "schedule_template_version": schedule_template_version  # New filter added
        },
        fields=["lesson_day", "from_time", "course", "group", "room", "instructor"]
    )

    # Populate the schedule
    for lesson in lesson_templates:
        day = lesson["lesson_day"].capitalize()  # Capitalize day to match days format
        from_time = time_mapping.get(lesson["from_time"], "")  # Map time to range
        course = lesson["course"]
        group = lesson["group"]
        room = lesson["room"]
        instructor_name = lesson["instructor"]

        # Format the content as a dictionary to easily access it later
        lesson_data = {
            "group": group,
            "course": course,
            "instructor": instructor_name,
            "room": room
        }

        if day in lessons and from_time in time_slots:
            index = time_slots.index(from_time)
            lessons[day][index] = lesson_data  # Store the lesson data in the appropriate slot

    return lessons
