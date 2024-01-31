// // Copyright (c) 2024, SanU and contributors
// // For license information, please see license.txt

// // frappe.ui.form.on("Topic", {
// // 	refresh(frm) {

// // 	},
// // });  



frappe.ui.form.on("Topic", {
    onload_post_render: function (frm) {
        frm.doc.applicants.forEach(function (applicant) {
            retrieve_applicant(frm, applicant.doctype, applicant.name, applicant);
        });
    },
    topic_main_category(frm) {
        // Update the options for the sub-category field based on the selected main category
        frm.set_query("topic_sub_category", function () {
            return {
                filters: {
                    topic_main_category: frm.doc.topic_main_category
                }
            };
        });
    },
});




frappe.ui.form.on("Topic Applicant", {
    applicant: async function (frm, cdt, cdn) {
        // Get the topic applicant document
        let topic_applicant = frappe.get_doc(cdt, cdn);
        // Retrieve the applicant document from the server
        retrieve_applicant(frm, cdt, cdn, topic_applicant);


        //get current applicant 
        let row = locals[cdt][cdn];

        // Call the check_applicant_duplicate function to check for duplicate 
        await check_applicant_duplicate(row);


        /**
         * Check for duplicate applicants in the child table
         * @param {Object} row - The child table row to check for duplicates
         */
        async function check_applicant_duplicate(row) {
            // Array to store unique applicant users
            let unique_applicant_users = [];
            // Check if there are existing applicants in the parent doctype
            if (frm.doc.applicants) {
                // Iterate through each applicant in the parent doctype
                for (let applicant of frm.doc.applicants) {
                    // Get the applicant user using the get_applicant_user function
                    let applicant_user = await get_applicant_user(applicant);
                    applicant_user = applicant_user.message;
                    // Check for duplicates
                    if (unique_applicant_users.includes(applicant_user)) {
                        // Duplicate found
                        frappe.msgprint_dialog = frappe.msgprint(__("Duplicate applicant: {0}", [applicant.applicant_name]));
                        row.applicant = ""; // Clear the applicant field in the current row
                        row.applicant_name = "";
                        frm.refresh_field("applicants");
                    } else {
                        // Unique value pushed to the array
                        unique_applicant_users.push(applicant_user);
                    }
                }
            }
        }

        /**
            * This function fetch the user value from the user field of the applicant ,then return it 
        * */
        function get_applicant_user(applicant) {
            return frappe.call({
                method: "academia.councils.doctype.topic.topic.get_applicant_user",
                args: {
                    applicant_type: applicant.applicant_type,
                    applicant: applicant.applicant
                },
            });
        }
    }

});

/**
 * Retrieves an applicant document and sets the applicant name field on the form with the retrieved value.
 *
 * @param {Object} frm - The form object.
 * @param {string} cdt - The child doctype name.
 * @param {string} cdn - The child document name.
 * @param {Object} applicant - The applicant object containing the applicant type and ID.
 * @returns {void}
 */
function retrieve_applicant(frm, cdt, cdn, applicant) {
    // Retrieve the document using frappe.call
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: applicant.applicant_type,
            name: applicant.applicant
        },
        callback: function (response) {
            let applicant_document = response.message; // Extract the applicant document from the response
            if (applicant_document) {
                let applicant_full_name = applicant_document.full_name;
                // Set the value of the 'applicant_name' field
                frappe.model.set_value(cdt, cdn, 'applicant_name', applicant_full_name);
                frm.refresh_field('applicant_name'); // Refresh the field on the form
            } else {
                console.log("Document not found");
            }
        }
    });
}
