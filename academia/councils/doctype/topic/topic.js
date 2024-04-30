// // Copyright (c) 2024, SanU and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Topic", {
  onload_post_render: function (frm) {
    if (frm.doc.__islocal) {
      return; // Do not execute if the document is fresh or it is the first time created
    }
    frm.doc.applicants.forEach(function (applicant) {
      // populate applicant name post render
      populate_applicant_full_name(
        frm,
        applicant.doctype,
        applicant.name,
        applicant
      );
    });
  },
  topic_main_category(frm) {
    // Update the options for the sub-category field based on the selected main category
    frm.set_query("topic_sub_category", function () {
      return {
        filters: {
          topic_main_category: frm.doc.topic_main_category,
        },
      };
    });
  },
  refresh(frm) {
    // Add a custom button to assign the topic to a council
    if (
      doc.__onload &&
      doc.__onload.has_topic_assignment != false &&
      frm.doc.docstatus === 1
    ) {
      frm.add_custom_button(__("Assign to Council"), function () {
        frappe.new_doc("Topic Assignment", {
          topic: frm.doc.name,
          title: frm.doc.title,
          descripition: frm.doc.descripition,
          council: frm.doc.council,
        });
      });
    }
  },
});

frappe.ui.form.on("Topic Applicant", {
  applicant: function (frm, cdt, cdn) {
    // Retrieve and update form with the applicant name
    let topic_applicant = frappe.get_doc(cdt, cdn);

    if (topic_applicant.applicant) {
      // Attempt to check for duplicates after ensuring applicant list is updated
      try {
        check_for_duplicate_applicant(frm, cdt, cdn);
      } catch (error) {
        frappe.msgprint(
          __("Failed to verify duplicate applicants: " + error.message)
        );
      }
    }
    if (topic_applicant.applicant) {
      populate_applicant_full_name(frm, cdt, cdn, topic_applicant);
    }
  },
});

/**
 * Checks for duplicate applicants
 * to ensure that there are no duplicate entries with the same applicant and applicant type.
 * If a duplicate is found, it clears the duplicate applicant fields and displays a message.
 *
 * @param {object} frm - The current form object.
 * @param {string} cdt - The child doctype (child table name).
 * @param {string} cdn - The name of the child doctype record (unique identifier for the row).
 */
function check_for_duplicate_applicant(frm, cdt, cdn) {
  var row = locals[cdt][cdn]; // Access the specific row in the child table using the locals object.
  // Filter the child table rows to find any other rows with the same applicant and applicant type.
  var duplicates = frm.doc.applicants.filter(function (d) {
    return (
      d.applicant === row.applicant &&
      d.applicant_type === row.applicant_type &&
      d.name !== row.name
    );
  });
  // If duplicates are found, display a message and clear the fields to correct the entry.
  if (duplicates.length > 0) {
    frappe.msgprint(
      __("Duplicate entry for Applicant: {0} of Type: {1}", [
        row.applicant,
        row.applicant_type,
      ])
    );
    frappe.model.set_value(cdt, cdn, "applicant_name", ""); // Additionally, clear the duplicate applicant name field.
    frappe.model.set_value(cdt, cdn, "applicant", ""); // Clear the duplicate applicant ID field.
  }
}

/**
 * Fetches details for a specified applicant based on their type and ID, then updates a field in a child document with the applicant's full name.
 *
 * This function asynchronously calls the backend to retrieve an applicant's document from the database. Upon successfully fetching the document, it extracts the applicant's full name and updates the 'applicant_name' field in the specified child document of the form. If the document cannot be found, it logs a message indicating the document was not found.
 * @param {Object} frm - The current form object, providing context for where the update needs to occur.
 * @param {string} cdt - The name of the child doctype, indicating where within the form the update should be made.
 * @param {string} cdn - The name of the child document, specifying the exact document to be updated.
 * @param {Object} applicant - An object containing details about the applicant, specifically their type and unique ID, used to retrieve the correct document.
 * @returns {void} - This function does not return a value.
 */
function populate_applicant_full_name(frm, cdt, cdn, applicant) {
  // Retrieve the document using frappe.call
  frappe.call({
    method: "frappe.client.get",
    args: {
      doctype: applicant.applicant_type,
      name: applicant.applicant,
    },
    callback: function (response) {
      let applicant_document = response.message; // Extract the applicant document from the response
      if (applicant_document) {
        let applicant_full_name =
          applicant_document.first_name + " " + applicant_document.last_name;
        // Set the value of the 'applicant_name' field
        frappe.model.set_value(cdt, cdn, "applicant_name", applicant_full_name);
      } else {
        console.log("Document not found");
      }
    },
  });
}
