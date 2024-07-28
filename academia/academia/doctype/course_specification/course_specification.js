// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Course Specification", {
    refresh: function(frm) {
        frm.fields_dict['credit_hours'].grid.get_field('hour_type').get_query = function(doc, cdt, cdn) {
            let selected_hour_types = frm.doc.credit_hours.map(row => row.hour_type);
            return{
                filters: [
                    ['name', 'not in', selected_hour_types]
                ]
            };
        };
    },

});
