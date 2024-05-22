// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Academic Program", {
	program_degree: function(frm) {
        if (frm.doc.program_degree === 'Master Degree' || frm.doc.program_degree === 'PHD Degree') {
            frm.toggle_display(['courses','research_or_thesis'], true);
            frm.set_value('minimum_course_average_to_start_research', '');
            frm.set_value('minimum_research_period', '');
            frm.set_value('maximum_research_period', '');
        }
        else{
            frm.toggle_display(['courses','research_or_thesis'], false);
            frm.set_value('courses', false);
            frm.set_value('research_or_thesis', false);
            frm.set_value('minimum_course_average_to_start_research', '');
            frm.set_value('minimum_research_period', '');
            frm.set_value('maximum_research_period', '');

        }
    }
});

    cur_frm.cscript.custom_validate = function(){
        if (cur_frm.doc.__islocal) return;

        if(cur_frm.doc.program_degree !== cur_frm.doc.__original.program_degree){
            cur_frm.set_value('courses', false);
            cur_frm.set_value('research_or_thesis', false);
        }

    };
