// Copyright (c) 2024, SanU Development Team and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transaction Category', {
    refresh: function(frm) {
        // Filter the "Parent Transaction Category" field choices
        frm.fields_dict['category_parent'].get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['Transaction Category', 'category_parent', '=', ''],  // Only show parties without a parent
                    ['Transaction Category', 'name', '!=', doc.name]  // Exclude the current item
                ]
            };
        };
    },
    category_parent: function (frm) {
        if (frm.doc.category_parent) {
            frappe.call({
              method: "academia.transaction_management.doctype.transaction.transaction.get_transaction_category_requirement",
              args: {
                transaction_category: frm.doc.category_parent
              },
              callback: function(response) {
                // Add attach image fields for each Transaction Type Requirement
                const requirements = response.message || [];
                console.log(requirements[0]);
                requirements.forEach(function(requirement) {
                  frm.add_child("requirements", {
                    requirement_name: requirement.name,
                    file_type: requirement.file_type,
                    required: requirement.required
                  });
                });
              }
            });
          }
    }
});