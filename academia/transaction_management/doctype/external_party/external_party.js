// Copyright (c) 2024, SanU Development Team and contributors
// For license information, please see license.txt

frappe.ui.form.on('External Party', {
    refresh: function(frm) {
        // Filter the "Parent External Party" field choices
        frm.fields_dict['parent_external_party'].get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['External Party', 'parent_external_party', '=', ''],  // Only show parties without a parent
                    ['External Party', 'name', '!=', doc.name]  // Exclude the current item
                ]
            };
        };
    }
});



