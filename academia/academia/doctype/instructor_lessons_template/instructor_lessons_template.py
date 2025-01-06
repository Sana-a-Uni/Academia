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
		group: DF.Link | None
		instructor: DF.Link | None
		program_specification: DF.Link | None
		room: DF.Link | None
		schedule_template_version: DF.Link | None
		schedule_type: DF.Literal["", "Instructor", "Group", "Room", "All Instructor", "All Group", "All Room"]
	# end: auto-generated types


@frappe.whitelist()
def get_lessons_data(schedule_type, identifier=None, faculty=None, schedule_template_version=None):
	"""
	Fetch lessons based on the selected schedule type (Instructor, Group, Room, or All)
	"""
	lessons = {}
	days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
	time_slots = ["08:00 - 10:00", "10:00 - 12:00", "12:00 - 14:00", "14:00 - 16:00", "16:00 - 18:00"]

	# Initialize an empty schedule for each day and time slot
	for day in days:
		lessons[day] = [None] * len(time_slots)

	# Mapping for time ranges
	time_mapping = {
		"8": "08:00 - 10:00",
		"10": "10:00 - 12:00",
		"12": "12:00 - 14:00",
		"14": "14:00 - 16:00",
		"16": "16:00 - 18:00",
	}

	filters = {
		"faculty": faculty,
		"schedule_template_version": schedule_template_version,
	}

	# Adjust filters based on `schedule_type`
	if schedule_type in ["Instructor", "Group", "Room"] and identifier:
		filters[schedule_type.lower()] = identifier
	elif schedule_type in ["All Instructor", "All Group", "All Room"]:
		schedule_type = schedule_type.split(" ")[1]  # Extract type (Instructor, Group, Room)

	# Fetch lessons
	lesson_templates = frappe.get_all(
		"Lesson Template",
		filters=filters,
		fields=["lesson_day", "from_time", "course", "group", "room", "instructor"],
	)

	# Group lessons based on schedule_type
	lessons_grouped = {}
	for lesson in lesson_templates:
		key = lesson[schedule_type.lower()]  # Group by Instructor/Group/Room
		if key not in lessons_grouped:
			lessons_grouped[key] = {day: [None] * len(time_slots) for day in days}

		day = lesson["lesson_day"].capitalize()
		from_time = time_mapping.get(lesson["from_time"], "")
		lesson_data = {
			"group": lesson["group"],
			"course": lesson["course"],
			"instructor": lesson["instructor"],
			"room": lesson["room"],
		}

		if day in lessons_grouped[key] and from_time in time_slots:
			index = time_slots.index(from_time)
			lessons_grouped[key][day][index] = lesson_data

	return lessons_grouped
