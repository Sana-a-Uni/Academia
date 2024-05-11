// // Copyright (c) 2024, SanU and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Topic", {
  refresh(frm) {
    // Add a custom button to assign the topic to a council
    if (
      frm.doc.__onload &&
      frm.doc.__onload.has_topic_assignment != false &&
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
      populate_applicant_full_name(cdt, cdn, topic_applicant);
    }
  },
  applicant_type: function (frm, cdt, cdn) {
    frappe.model.set_value(cdt, cdn, "applicant", "");
    frappe.model.set_value(cdt, cdn, "applicant_name", "");
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

function populate_applicant_full_name(cdt, cdn, applicant) {
  frappe.db
    .get_value(applicant.applicant_type, { name: applicant.applicant }, [
      "first_name",
      "last_name",
    ])
    .then(function (values) {
      if (values) {
        let applicant_full_name =
          values.message.first_name + " " + values.message.last_name;
        // Set the value of the 'applicant_name' field
        frappe.model.set_value(cdt, cdn, "applicant_name", applicant_full_name);
      }
    });
}
