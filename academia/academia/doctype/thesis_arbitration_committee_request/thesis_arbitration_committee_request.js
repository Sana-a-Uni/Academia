
frappe.ui.form.on("Thesis Arbitration Committee Request", {
    on_submit: function(frm) {
        // Define the applicants array with the faculty member details
        let applicants = [
            {
                applicant_type: "Faculty Member",
                applicant: frm.doc.faculty_member,
                applicant_name: frm.doc.faculty_member_name
            }
        ];
        // Convert the applicants array to a JSON string
        applicants = JSON.stringify(applicants);

        // Make a Frappe call to create the transaction
        frappe.call({
            method: "academia.transaction_management.doctype.transaction.transaction.create_transaction",
            args: {
                priority: "",
                title: "Thesis Arbitration Committee Request",
                category: "Faculty Member",
                sub_category: "Thesis Arbitration Committee Request",
                refrenced_document: frm.doc.name,
                applicants_list: applicants
            },
            callback: function(r) {
                // Log the response object to the console for debugging
                console.log(r);

                // Check if the response contains the 'message' property (transaction ID)
                if (r && r.message) {
                    // Set the transaction ID in the 'referenced_transaction' field
                    frm.set_value("referenced_transaction", r.message);

                    // Navigate to the transaction
                    go_to_transaction(r.message, applicants, frm);
                } else {
                    // Log an error if the response format is unexpected
                    console.error("Unexpected response format");
                }
            }
        });
    },

    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Confirm Request'), function() {
                var new_doc = frappe.model.get_new_doc('Thesis Arbitration Committee');
                
                new_doc.faculty_member = frm.doc.faculty_member;
                new_doc.faculty_member_publication = frm.doc.faculty_member_publication;
                new_doc.reference_doctype = frm.doc.doctype;
                new_doc.document_name = frm.doc.name;
                
                new_doc.internal_arbitration_committee = [];
                frm.doc.internal_arbitration_committee.forEach(function(row) {
                    var new_row = frappe.model.add_child(new_doc, 'Internal Arbitration Committee', 'internal_arbitration_committee');
                    new_row.faculty = row.faculty;
                    new_row.academic_rank = row.academic_rank;
                    new_row.faculty_member = row.faculty_member;
                });
        
                new_doc.external_arbitration_committee = [];
                frm.doc.external_arbitration_committee.forEach(function(row) {
                    var new_row = frappe.model.add_child(new_doc, 'External Arbitration Committee', 'external_arbitration_committee');
                    new_row.university = row.university;
                    new_row.external_faculty = row.external_faculty;
                    new_row.academic_rank = row.academic_rank;
                    new_row.faculty_member = row.faculty_member;
                });
                
                // Ensure the new document has a proper name
                frappe.db.insert(new_doc).then(function(response) {
                    frappe.set_route('Form', response.doctype, response.name);
                });
            });
        }
    }
});

// Function to navigate to the transaction
function go_to_transaction(transactionId, applicants, frm) {
    // Implement your logic to navigate to the transaction page
    frappe.set_route('Form', 'Transaction', transactionId);
}

frappe.ui.form.on("Internal Arbitration Committee", {
    faculty: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];

        // Clear the faculty member field when faculty changes
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        
        // Apply filtering logic
        filter_internal(frm, cdt, cdn);
    },

    academic_rank: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        // Clear the faculty_member field
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        
        // Apply filtering logic
        filter_internal(frm, cdt, cdn);
    },

    faculty_member: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        let duplicate = frm.doc.internal_arbitration_committee.some((r) => 
            r.faculty === row.faculty && 
            r.academic_rank === row.academic_rank && 
            r.faculty_member === row.faculty_member && 
            r.idx !== row.idx
        );

        if (duplicate) {
            frappe.msgprint(__('This Faculty Member is already selected. Please choose a different one.'));
            frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        }
    },

    internal_arbitration_committee_add: function(frm, cdt, cdn) {
        filter_internal(frm, cdt, cdn);
    }
});

frappe.ui.form.on("External Arbitration Committee", {
    university: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        // Clear the faculty_member and external_faculty fields
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        frappe.model.set_value(cdt, cdn, 'external_faculty', '');
        
        // Apply filtering logic
        filter_external(frm, cdt, cdn);
    },

    academic_rank: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        // Clear the faculty_member field
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        
        // Apply filtering logic
        filter_external(frm, cdt, cdn);
    },

    external_faculty: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        // Clear the faculty_member field
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        
        // Apply filtering logic
        filter_external(frm, cdt, cdn);
    },

    faculty_member: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        let duplicate = frm.doc.external_arbitration_committee.some((r) => 
            r.university === row.university && 
            r.external_faculty === row.external_faculty && 
            r.academic_rank === row.academic_rank && 
            r.faculty_member === row.faculty_member && 
            r.idx !== row.idx
        );

        if (duplicate) {
            frappe.msgprint(__('This Faculty Member with the same university, external faculty, and academic rank is already selected. Please choose a different one.'));
            frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        }
    },

    external_arbitration_committee_add: function(frm, cdt, cdn) {
        filter_external(frm, cdt, cdn);
    }
});

function filter_internal(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    frm.fields_dict['internal_arbitration_committee'].grid.get_field('faculty_member').get_query = function () {
        let filters = {
            'from_another_university': "",
            'external_faculty': ""
        };

        if (row.faculty) {
            filters['faculty'] = row.faculty;
        }

        if (row.academic_rank) {
            filters['academic_rank'] = row.academic_rank;
        }

        return { filters: filters };
    };
}

function filter_external(frm, cdt, cdn) {
    const row = locals[cdt][cdn];

    frm.fields_dict['external_arbitration_committee'].grid.get_field('faculty_member').get_query = function () {
        let filters = {};

        if (row.university) {
            filters['from_another_university'] = row.university;
        } else {
            filters['from_another_university'] = ['!=', ''];
        }

        if (row.external_faculty) {
            filters['external_faculty'] = row.external_faculty;
        } else {
            filters['external_faculty'] = ['!=', ''];
        }

        if (row.academic_rank) {
            filters['academic_rank'] = row.academic_rank;
        }

        return { filters: filters };
    };

    frm.fields_dict['external_arbitration_committee'].grid.get_field('external_faculty').get_query = function () {
        let filters = {};

        if (row.university) {
            filters['university'] = row.university;
        }

        return { filters: filters };
    };
}


