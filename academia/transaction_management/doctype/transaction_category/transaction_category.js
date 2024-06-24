// Copyright (c) 2024, SanU Development Team and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Transaction Category", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Transaction Category', {
    refresh: function(frm) {
        // Filter the "Parent Transaction Category" field choices
        frm.fields_dict['parent_category'].get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ["Transaction Category", "is_group", "=", 1],
                    ['Transaction Category', 'parent_category', '=', ''],  // Only show parties without a parent
                    // ['Transaction Category', 'name', '!=', doc.name]  // Exclude the current item
                ]
            };
        };
    },

    validate: function(frm) {
        // Validation for is_group checkbox
        if (frm.doc.is_group) {
            // If is_group is checked, clear the parent_category field
            frm.set_value('parent_category', null);
            frm.refresh_field('parent_category');
        } else {
            // If is_group is not checked, ensure parent_category is not empty
            if (!frm.doc.parent_category) {
                frappe.throw(__("Parent Category is mandatory if 'Is Group' is not checked."));
            }
        }
    }  

});
