// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student Batch", {
	faculty: function(frm) {
        var faculty = frm.doc.faculty;
        frm.set_query("program", function() {
            return {
                "filters": {
                    "faculty": faculty
                }
            };
        });
        frm.set_query("program_specification", function(){
            return {
                "filters":{
                    "faculty": faculty
                }
            };
        });
        frm.set_value('program', '');
        frm.set_value('program_specification', '');
    }
});
