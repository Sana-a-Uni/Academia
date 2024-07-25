// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction Company Head", {
	refresh(frm) {
        frm.fields_dict['head_employee'].get_query = function(doc) {
            return {
                filters: {
                    'company': frm.doc.company
                }
            };
        };
	},
});
