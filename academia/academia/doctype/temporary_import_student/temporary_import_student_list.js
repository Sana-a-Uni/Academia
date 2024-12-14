frappe.listview_settings["Temporary Import Student"] = {
    onload: function (list_view) {
        list_view.page.add_inner_button(__("Enroll Students"), function () {
            // Show progress bar
            frappe.show_progress(__('Enrolling Students'), 0, 100);

            // Subscribe to progress updates
            frappe.realtime.on('enrollment_progress', function(data) {
                frappe.show_progress(__('Enrolling Students'), data.percentage, 100);
            });

            frappe.call({
                method: "academia.academia.doctype.temporary_import_student.temporary_import_student.enroll_students",
                callback: function (r) {
                    // Hide progress bar
                    frappe.hide_progress();

                    if (!r.exc) {
                        frappe.msgprint(__("Students have been successfully enrolled."));
                        list_view.refresh();  // Refresh the list view after enrollment
                    }

                    // Unsubscribe from progress updates
                    frappe.realtime.off('enrollment_progress');
                },
                // Ensure to hide the progress bar in case of error as well
                error: function () {
                    frappe.hide_progress();
                    frappe.msgprint(__("An error occurred during enrollment."));
                    frappe.realtime.off('enrollment_progress');
                }
            });
        });
    },
};