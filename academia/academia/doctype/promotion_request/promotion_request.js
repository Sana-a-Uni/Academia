frappe.ui.form.on("Promotion Request", {
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
                title: "Promotion Request",
                category: "Faculty Member",
                sub_category: "Promotion Request",
                refrenced_document: frm.doc.name,
                applicants_list: applicants
            },
            callback: function(r) {
                // Log the response object to the console for debugging
                console.log(r);

                // Check if the response contains the 'message' property
                if (r && r.message) {
                    // Access the transaction ID from the response
                    const transactionId = r.message;
                    // Optionally, show a message with the transaction ID
                    // frappe.msgprint("Transaction ID: " + transactionId);

                    // Set the transaction ID in the 'referenced_transaction' field
                    frm.set_value("referenced_transaction", transactionId);

                    // Navigate to the transaction
                    go_to_transaction(transactionId, applicants, frm);
                } else {
                    // Log an error if the response format is unexpected
                    console.error("Unexpected response format");
                }
            }
        });
    }
});

// Function to navigate to the transaction
function go_to_transaction(transactionId, applicants, frm) {
    // Implement your logic to navigate to the transaction page
    // You can use `frappe.set_route` or any other method as required
    frappe.set_route('Form', 'Transaction', transactionId);
}


// frappe.ui.form.on("Promotion Request", {
//     refresh: function(frm) {
//         // Initialize filters when the form is refreshed
//         frm.fields_dict['academic_arbitrators'].grid.get_field('arbitrator_name').get_query = function(doc, cdt, cdn) {
//             const row = locals[cdt][cdn];
//             return {
//                 filters: {
//                     'from_another_university': row.university || ''
//                 }
//             };
//         };
//     },

//     university: function(frm, cdt, cdn) {
//         const row = locals[cdt][cdn];

//         // Clear the arbitrator_name field when the university changes
//         frappe.model.set_value(cdt, cdn, 'arbitrator_name', '');
        
//         // Apply filtering logic to the arbitrator_name field
//         frm.fields_dict['academic_arbitrators'].grid.get_field('arbitrator_name').get_query = function(doc, cdt, cdn) {
//             return {
//                 filters: {
//                     'from_another_university': row.university || ''
//                 }
//             };
//         };
        
//         // Refresh the grid to apply the new filter
//         frm.fields_dict['academic_arbitrators'].grid.refresh();
//     },

//     arbitrator_name: function(frm, cdt, cdn) {
//         const row = locals[cdt][cdn];
//         let duplicate = frm.doc.academic_arbitrators.some((r) => 
//             r.university === row.university && 
//             r.arbitrator_name === row.arbitrator_name && 
//             r.idx !== row.idx
//         );

//         if (duplicate) {
//             frappe.msgprint(__('This Arbitrator is already selected in this university. Please choose a different one.'));
//             frappe.model.set_value(cdt, cdn, 'arbitrator_name', '');
//         }
//     },

//     academic_arbitrators_add: function(frm, cdt, cdn) {
//         // Apply the filtering logic to newly added rows
//         const row = locals[cdt][cdn];
//         frm.fields_dict['academic_arbitrators'].grid.get_field('arbitrator_name').get_query = function(doc, cdt, cdn) {
//             return {
//                 filters: {
//                     'from_another_university': row.university || ''
//                 }
//             };
//         };
        
//         // Refresh the grid to apply the new filter
//         frm.fields_dict['academic_arbitrators'].grid.refresh();
//     }
// });


// frappe.ui.form.on("Promotion Request", {
//     refresh: function(frm) {
//         // Initially hide the university field
//         frm.toggle_display('university', false);
//     },

//     arbitrator_name: function(frm) {
//         if (frm.doc.arbitrator_name) {
//             frappe.db.get_value('Faculty Member', frm.doc.arbitrator_name, 'from_another_university')
//                 .then(r => {
//                     if (r.message && r.message.from_another_university) {
//                         // Show the university field if from_another_university has a value
//                         frm.toggle_display('university', true);
//                     } else {
//                         // Hide the university field if from_another_university is empty
//                         frm.toggle_display('university', false);
//                     }
//                 }).catch(err => {
//                     console.error(err);
//                 });
//         } else {
//             // Hide the university field if no arbitrator_name is selected
//             frm.toggle_display('university', false);
//         }
//     }
// });
