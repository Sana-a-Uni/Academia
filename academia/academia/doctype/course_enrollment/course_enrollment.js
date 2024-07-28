// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Course Enrollment", {
	faculty: function(frm) {
        var faculty = frm.doc.faculty;
        frm.set_query("faculty_department", function() {
            return {
                "filters": {
                    "faculty": faculty
                }
            };
        });
        frm.set_query("academic_program", function(){
            return {
                "filters":{
                    "faculty": faculty
                }
            };
        });
        frm.set_query("student_batch", function(){
            return {
                "filters":{
                    "faculty": faculty
                }
            };
        });
        frm.set_value('faculty_department', '');
        frm.set_value('academic_program', '');
        frm.set_value('student_batch', '');
    }
});
