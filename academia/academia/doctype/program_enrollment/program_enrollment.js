// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Program Enrollment", {
	faculty: function(frm) {
        var faculty = frm.doc.faculty;
        frm.set_query("program", function() {
            return {
                "filters": {
                    "faculty": faculty
                }
            };
        });
    },
   
});
