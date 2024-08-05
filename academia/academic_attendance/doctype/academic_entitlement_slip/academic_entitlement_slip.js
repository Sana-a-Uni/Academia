// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Academic Entitlement Slip", {
	refresh(frm) {

	},

    faculty(frm) {

        frm.trigger("reset_fields")       
    },

    start_date(frm) {

        frm.trigger("reset_fields")       
    },
    end_date(frm) {

        frm.trigger("reset_fields")       
    },
    hour_rate_list(frm) {

        frm.trigger("reset_fields")       
    },
    academic_term(frm) {

        frm.trigger("reset_fields")       
    },
    academic_year(frm) {

        frm.trigger("reset_fields")       
    },


    reset_fields(frm) {

		frm.set_value("details", []);
    },


});


// frappe.ui.form.on("Academic Entitlement Slip", {
//     "get_academic_entitlement_details": function(frm) {
// 		frm.set_value("details",[]);
// 		frappe.call({
// 			method: "get_academic_entitlement_details",
// 			doc:frm.doc,
// 			callback: function(r) {
// 					frm.set_value( r.message.courses);
// 			}
// 		});
//     },
//     });
