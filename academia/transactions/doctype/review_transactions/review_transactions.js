// Copyright (c) 2025, SanU and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Review Transactions", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Transactions For Review", {
    form_render: function (frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        let document_type = child.document_type;
        
        // Dynamically set the query for the document_name field
        frm.fields_dict['document_name'].grid.get_field("document_name").get_query = function() {
            return {
                query: "academia.transactions.doctype.review_transactions.review_transactions.get_documents",
                filters: {
                    docstatus: 1,  // Only include submitted documents
                    document_type: document_type,  // Use the document_type from the child row
                    company: frm.doc.company  // Pass company from the parent form
                }
            };
        };

        // If needed, trigger any additional logic here for the row
        // For example, refreshing the field or showing messages
        frm.refresh_field("document_name");
    },
    
    document_name: function (frm, cdt, cdn) {
        console.log("Triggered document_name");
        let child = locals[cdt][cdn];
        console.log("Child Object:", child);

        if (child.document_type) {
            frappe.db.get_value(
                child.document_type,
                child.document_name,
                "title",
                function (r) {
                    console.log("Response:", r);
                    if (r) {
                        frappe.model.set_value(cdt, cdn, "document_title", r.title);
                    } else {
                        frappe.msgprint(
                            `Title not found for the selected ${child.document_type}.`
                        );
                    }
                }
            );
        } else {
            frappe.msgprint("Please select a Document Type first.");
        }
    },
});
