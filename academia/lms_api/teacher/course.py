import frappe
from datetime import datetime
from collections import defaultdict

@frappe.whitelist()
def get_faculty_member_from_user(user_id):
    employee = frappe.get_value("Employee", {"user_id": user_id}, "name")
    if not employee:
        raise frappe.ValidationError("Employee not found for the user.")
    
    faculty_member = frappe.get_value("Faculty Member", {"employee": employee}, "name")
    if not faculty_member:
        raise frappe.ValidationError("Faculty member not found for the employee.")
    
    return faculty_member

@frappe.whitelist()
def get_current_term_and_academic_year():
    try:
        user_id = frappe.session.user
        faculty_member_id = get_faculty_member_from_user(user_id)
        
        # Get faculty for the faculty member
        faculty = frappe.get_value("Faculty Member", faculty_member_id, "faculty")
        
        now = datetime.now().date()
        
        # Query to get the current academic year
        academic_year = frappe.db.sql("""
            SELECT name as academic_year
            FROM `tabAcademic Year`
            WHERE %s BETWEEN year_start_date AND year_end_date
            AND disabled = 0
            LIMIT 1
        """, (now,), as_dict=1)
        
        if not academic_year:
            return {"error": "No active academic year found for the current date"}

        academic_year_name = academic_year[0]['academic_year']

        # Query to get the current term based on the academic year and faculty
        term = frappe.get_all(
            'Academic Term',
            filters={
                'academic_year': academic_year_name,
                'faculty': faculty,
                'disabled': 0  # Exclude disabled terms
            },
            fields=['term_name', 'academic_year']
        )

        if term:
            return {"term": term[0]['term_name'], "academic_year": term[0]['academic_year']}
        else:
            return {"error": "No active term found for the specified faculty and current academic year"}
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in get_current_term_and_academic_year")
        return {"error": str(e)}

@frappe.whitelist()
def get_faculty_details_for_current_term_and_year():
    try:
        # Get current term and academic year
        term_and_year = get_current_term_and_academic_year()
        if 'error' in term_and_year:
            return term_and_year

        term = term_and_year['term']
        academic_year = term_and_year['academic_year']
        
        user_id = frappe.session.user
        faculty_member_id = get_faculty_member_from_user(user_id)

        # Query to get all details for the faculty member for the specified term and academic year
        assignments = frappe.get_all(
            'Group Assignment',
            filters={
                'instructor': faculty_member_id,
                'academic_year': academic_year,
                'academic_term': term
            },
            fields=['academic_year', 'faculty', 'academic_term', 'program', 'student_batch', 'group', 'course']
        )

        # Fetch additional course details and program name
        for assignment in assignments:
            course_details = frappe.get_value('Course Study', assignment['course'], ['course_type','course_name', 'level'], as_dict=True)
            program_name = frappe.get_value('Program Specification', assignment['program'], 'program_name')
            assignment.update(course_details)
            assignment['program_name'] = program_name

        # Merge similar assignments
        merged_assignments = defaultdict(lambda: {
            "program_student_batch_group": set(),
            "courses": set()
        })

        for assignment in assignments:
            key = (
                assignment['course_name'],
                assignment['academic_year'],
                assignment['academic_term'],
                assignment['course_type'],
                assignment['faculty']
            )
            program_student_batch_group = (assignment["program_name"], assignment["student_batch"], assignment["group"])
            merged_assignments[key]["program_student_batch_group"].add(program_student_batch_group)
            merged_assignments[key]["courses"].add(assignment["course"])

        merged_assignments_list = []
        for key, value in merged_assignments.items():
            course_name, academic_year, academic_term, course_type, faculty = key
            program_student_batch_group = [
                {"program": p, "student_batch": s, "group": g}
                for p, s, g in value["program_student_batch_group"]
            ]
            merged_assignments_list.append({
                "course_name": course_name,
                "academic_year": academic_year,
                "academic_term": academic_term,
                "course_type": course_type,
                "faculty": faculty,
                "program_student_batch_group": program_student_batch_group,
                "course": ', '.join(value["courses"])
            })

        return merged_assignments_list
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in get_faculty_details_for_current_term_and_year")
        return {"error": str(e)}
