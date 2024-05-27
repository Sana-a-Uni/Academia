// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Council Memo", {
  refresh(frm) {
    // Add a custom button to assign the topic to a council
    if (frm.doc.docstatus === 1) {
      frm.add_custom_button(__("Create Assignment"), function () {
        frappe.new_doc("Topic Assignment", {
          council: frm.doc.council,
        });
      });
    }
  },
});
