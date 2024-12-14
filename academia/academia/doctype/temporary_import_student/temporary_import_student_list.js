frappe.listview_settings["Temporary Import Student"] = {
    onload: function (list_view) {
        list_view.page.add_inner_button(__("Enroll Students"), function () {
            // Show progress bar
            frappe.show_progress(__('Enrolling Students'), 0, 100);

            // Initialize a variable to track the total number of students
            let totalStudents = 0;

            // First, get the total number of students to enroll
            frappe.call({
                method: "academia.academia.doctype.temporary_import_student.temporary_import_student.get_total_students", // Create this method to get the total
                callback: function (r) {
                    totalStudents = r.message; // Assume this returns the total count

                    // Subscribe to progress updates
                    frappe.realtime.on('enrollment_progress', function(data) {
                        const currentProgress = data.percentage;
                        const currentCount = Math.round((currentProgress / 100) * totalStudents);
                        frappe.show_progress(__('Enrolling Students'), currentProgress, 100);
                        frappe.msgprint(__("Enrolled {0} of {1} students.", [currentCount, totalStudents]));
                    });

                    // Call the enrollment method
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
                        error: function () {
                            frappe.hide_progress();
                            frappe.msgprint(__("An error occurred during enrollment."));
                            frappe.realtime.off('enrollment_progress');
                        }
                    });
                }
            });
        });
    },
};