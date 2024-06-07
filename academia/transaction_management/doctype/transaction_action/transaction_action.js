// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction Action", {
    onload: function(frm) {
        // Set the initial visibility of the to_section
        frm.toggle_display("to_section", frm.doc.type === "Redirected");
    },
    type: function(frm) {
        // Toggle the visibility of the to_section when the type changes
        frm.toggle_display("to_section", frm.doc.type === "Redirected");
    }
});