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


    // error: there is a problem because of uniqe name
    // parent_category_: function(frm) {

    //     if (frm.doc.parent_category) {
    //       frappe.call({
    //         method: "academia.transaction_management.doctype.transaction.transaction.get_transaction_category_requirement",
    //         args: {
    //           transaction_category: frm.doc.parent_category
    //         },
    //         callback: function(response) {
    //           // Add attach image fields for each Transaction Type Requirement
    //           const requirements = response.message || [];
  
    //           requirements.forEach(function(requirement) {
    //             console.log(requirement)
    //             frm.add_child("requirements", {
    //               requirement_name: requirement.name,
    //               fieldtype: "Attach Image",
    //               file_type: requirement.file_type,
    //               required: requirement.required,
    //             });
    //           });
  
    //         // Refresh the form to display the newly added fields
    //            frm.refresh_fields("requirements");
    //         }
    //       });
    //     }
    //   },
  

});
