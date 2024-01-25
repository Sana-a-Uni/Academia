// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Council", {
    // Setup function called when the Council form is loaded
    setup: function (frm) {
        // Function to check for duplicate members
        frm.check_member_duplicate = function (frm, row) {
            // Iterate through each member in the form's members field
            frm.doc.members.forEach(member => {
                // Check if the current row's faculty_member is not empty or the same as the current member being iterated
                if (!(row.faculty_member == '' || row.idx == member.idx)) {
                    // Check if the current row's faculty_member is the same as the member's faculty_member
                    if (row.faculty_member == member.faculty_member) {
                        // Clear the faculty_member value in the current row
                        row.faculty_member = '';
                        // Refresh the members field in the form to reflect the changes
                        frm.refresh_field('members');
                        // message indicating that the member name already exists in a specific row
                        msgprint(__(`${member.member_name} already exists in row ${member.idx}`));
                    }
                }
            });
        }
    },
});

frappe.ui.form.on('Council Member', {
    // Event triggered when the faculty_member field changes in the Council Member form
    faculty_member: function (frm, cdt, cdn) {
        // Get the current row
        let row = locals[cdt][cdn];
        // Call the check_member_duplicate function to check for duplicate members
        frm.check_member_duplicate(frm, row);
    }
});