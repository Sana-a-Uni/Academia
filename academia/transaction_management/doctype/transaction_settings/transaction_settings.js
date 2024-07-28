// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction Settings", {
	refresh(frm) {
        frm.set_query("department", function(){
            return {
                filters: {
                    'company': frm.doc.company,
                }
            }
        });

	},
});
