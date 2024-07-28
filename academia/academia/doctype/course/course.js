// Copyright (c) 2023, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Course", {
	faculty: function(frm) {
        var faculty = frm.doc.faculty;
        frm.set_query("program", function() {
            return {
                "filters": {
                    "faculty": faculty
                }
            };
        });
        frm.set_value('program', '');
    },
    before_save: function(frm){
        if(frm.doc.course_type === 'University Requirement' || frm.doc.course_type === 'Faculty Requirement'){
            frm.set_value('program', '');
        }
            
    }
});
