// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt


frappe.ui.form.on("Lesson Attendance", {
	refresh(frm) {
        if(frm.doc.status == "Absent" && frm.doc.docstatus == 1) {
            frm.add_custom_button('Create Compensatory Lesson', () => {
                frappe.new_doc('Compensatory Lesson', {
                    lesson_attendance: frm.doc.name,
                    is_transfer: "1",
                    faculty: frm.doc.faculty,
                    academic_year: frm.doc.academic_year,
                    academic_term: frm.doc.academic_term,
                    program: frm.doc.program,
                    level: frm.doc.level,
                    instructor: frm.doc.faculty_member,
                    course_type: frm.doc.course_type,
                    course: frm.doc.course,
                    group: frm.doc.group,
                    subgroup:frm.doc.subgroup
                })
            })
        }

	},
});