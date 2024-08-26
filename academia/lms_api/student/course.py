import frappe

@frappe.whitelist()
def get_student_program_details():
    user_id = frappe.session.user
    student_id = frappe.get_value("Student", {"user_id": user_id}, "name")
    student_name = frappe.get_value("Student", {"user_id": user_id}, "full_name")
    
    if not student_id:
        return {"error": "Student not found for the current user."}
    
    # Fetch basic student program details
    student_program_details = frappe.db.sql("""
        SELECT 
            pe.student AS student_id,
            pe.student_name,
            pe.academic_year,
            pe.academic_term,
            sb.batch_name,
            sb.current_level,
            ps.name AS program_name,
            ps.faculty_department
        FROM 
            `tabProgram Enrollment` pe
        JOIN 
            `tabStudent Batch` sb ON pe.student_batch = sb.name
        JOIN 
            `tabProgram Specification` ps ON pe.program = ps.name
        WHERE 
            pe.student = %s
    """, (student_id,), as_dict=1)
    
    if not student_program_details:
        return {"error": "No program details found for the student."}
    
    # Extract current level and program name
    current_level = student_program_details[0]['current_level']
    program_name = student_program_details[0]['program_name']
    
    # Verify the extracted values
    if not current_level or not program_name:
        return {"error": "Current level or program name not found."}
    
    # Fetch courses based on the current level from Study Plan Course in Program Specification
    courses = frappe.db.sql("""
        SELECT 
            spc.course_code, 
            spc.course_name, 
            spc.course_type, 
            spc.elective
        FROM 
            `tabProgram Specification` ps
        JOIN 
            `tabStudy Plan Course` spc ON spc.parent = ps.name
        WHERE 
            ps.name = %s AND spc.study_level = %s
    """, (program_name, current_level), as_dict=1)
    
    # List to hold all courses with their hours
    all_courses = []

    # Fetch course hours for each course
    for course in courses:
        course_hours = frappe.db.sql("""
            SELECT 
                hour_type, 
                hours
            FROM 
                `tabCourse Hours`
            WHERE 
                parent = %s
        """, (course['course_code'],), as_dict=1)
        
        # Add hours to course details
        for hour in course_hours:
            all_courses.append({
                "course_code": course['course_code'],
                "course_name": course['course_name'],
                "elective": course['elective'],
                "course_type": hour['hour_type'],
                "hours": hour['hours']
            })
    
    # Verify the fetched courses
    if not all_courses:
        return {
            "student_details": student_program_details[0],
            "error": "No courses found for the current level in the program specification.",
            "current_level": current_level,
            "program_name": program_name,
            "student_name":student_name,
        }
    
    student_program_details[0]['courses'] = all_courses
    
    return student_program_details[0]
