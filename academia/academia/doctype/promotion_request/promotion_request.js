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


// Copyright (c) 2024, alaalsalam and contributors
// For license information, please see license.txt

// Copyright (c) 2024, alaalsalam and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Promotion Request", {
//     refresh(frm) {
//         // Set the query for the academic_publications field
//         frm.set_query("academic_publications", function (doc) {
//             return {
//                 filters: {
//                     name: ["in", getAcademicPublicationFilter(doc.faculty_member)]
//                 }
//             };
//         });
//     },

//     faculty_member: function(frm) {
//         // Update filter when the faculty member field changes
//         frm.set_query("academic_publications", function (doc) {
//             return {
//                 filters: {
//                     name: ["in", getAcademicPublicationFilter(doc.faculty_member)]
//                 }
//             };
//         });
//     }
// });



// function getAcademicPublicationFilter(faculty_member) {
//     if (faculty_member) {
//         frappe.call({
//             method: "academia.promotion_request.get_filtered_publications", // Path adjusted
//             args: {
//                 faculty_member: faculty_member
//             },
//             callback: function(response) {
//                 if (response.message) {
//                     let publication_names = response.message.map(publication => publication.name);
//                     console.log(publication_names); // Use or display the filtered publication names as needed
//                 }
//             },
//             error: function(err) {
//                 console.error("Error fetching filtered publications:", err);
//             }
//         });
//     }
// }




