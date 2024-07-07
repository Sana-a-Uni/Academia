// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Academic Program", {
    faculty: function(frm) {
        var faculty = frm.doc.faculty;
        frm.set_query("faculty_department", function() {
            return {
                "filters": {
                    "faculty": faculty
                }
            };
        });
    },

    program_degree: function(frm) {
        if (frm.doc.program_degree === 'Master Degree' || frm.doc.program_degree === 'PHD Degree') {
            frm.toggle_display(['courses', 'research_or_thesis'], true);
            frm.set_value('minimum_course_average_to_start_research', '');
            frm.set_value('minimum_research_period', '');
            frm.set_value('maximum_research_period', '');
        } else {
            frm.toggle_display(['courses', 'research_or_thesis'], false);
            frm.set_value('courses', false);
            frm.set_value('research_or_thesis', false);
            frm.set_value('minimum_course_average_to_start_research', '');
            frm.set_value('minimum_research_period', '');
            frm.set_value('maximum_research_period', '');

        }
    }
});

frappe.ui.form.on("Academic Program", "validate", function(frm) {
    if (frm.doc.__islocal) return;

    if (frm.doc.program_degree !== frm.doc.__original.program_degree) {
        frm.set_value('courses', false);
        frm.set_value('research_or_thesis', false);
    }
});
