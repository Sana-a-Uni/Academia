// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Course Study", {
	refresh(frm) {
        frm.set_query('academic_term', function() {
            if (frm.doc.academic_year) {
                return {
                    filters: {
                        'academic_year': frm.doc.academic_year
                    }
                };
            } else {
                return {};
            }
        });
	}
});
