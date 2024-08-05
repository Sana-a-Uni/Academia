// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Academic Hour Rate",  {
	change(frm) {

    },

  onload(frm) {
        
		frm.set_query("faculty_member", function(){
			return {
				"filters": {
					"faculty": frm.doc.faculty,
                    "academic_rank": frm.doc.academic_rank
				}
			}
		})
        
    },
    
    faculty(frm) {

        frm.trigger("reset_fields")       
    },

    academic_rank(frm) {

        frm.trigger("reset_fields")       
    },

    reset_fields(frm) {

		frm.set_value("faculty_member", "");
    },

 });
