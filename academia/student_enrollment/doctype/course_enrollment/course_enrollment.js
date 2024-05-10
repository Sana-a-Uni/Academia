// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Course Enrollment", {
    refresh(frm) {

    },
    before_save: function (frm) {
        // Get the value of the current doctype field
        const student_batch_Value = frm.doc.student_batch; // Replace 'student_batch' with the actual field name in your doctype

        // Fetch data from the linked doctype using the Frappe framework's API with a filter
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Course Study', // Replace 'Course Study' with the actual doctype you want to fetch data from
                fields: ['course_name'], // Replace 'course_name' with the field you want to display as checkbox label
                filters: [['student_batch', '=', student_batch_Value]], // Replace 'student_batch' with the actual field name in the linked doctype
                limit: 0 // Set the limit to fetch all records
            },
            callback: function (response) {
                // Handle the API response and create checkboxes
                const data = response.message;

                // Create an array to store the prompt fields
                const promptFields = [];

                data.forEach(function (item) {
                    const checkboxField = {
                        label: item.course_name, // Replace 'course_name' with the field you want to display as checkbox label
                        fieldname: item.course_name, // Replace 'course_name' with the field you want to use as the fieldname
                        fieldtype: 'Check'
                    };

                    promptFields.push(checkboxField);
                });

                // Display the prompt with checkboxes
                frappe.prompt(promptFields, function (values) {
                    // Handle the prompt values here
                    console.log(values);
                });
            }
        });
    }
});
