// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Session", {
    validate(frm) {
        frm.events.validate_time(frm);
        academia.councils.utils.validate_head_exist(frm.doc.members);
    },
    /**
     * Fetches the members of the selected council and adds them to the session form.
     * @param {object} frm - The current form object.
     */
    fetch_members_from_council(frm) {
        // Retrieve council form for selected council
        frappe.db.get_doc('Council', frm.doc.council).then(council => {
            if (council.members) {
                // Clear any existing members in the child table:
                frm.doc.members = '';
                // Loop through the council members and add them to the child table:
                council.members.forEach(council_member => {
                    frm.add_child('members', {
                        employee: council_member.employee,
                        attendance: 'Attend',
                        member_role: council_member.member_role
                    });
                });
                // Refresh the child table to display the new member:
                frm.refresh_field('members');
            }
        });
    },
    council(frm) {
        // Event handler for 'council' field change
        if (frm.doc.council) {
            // Fetch members from the selected council
            frm.trigger('fetch_members_from_council');
        }
    }
    ,
    validate_time(frm) {
        if (frm.doc.begin_time && frm.doc.end_time) {
            if (frm.doc.begin_time > frm.doc.end_time) {
                frappe.throw(__("End time must be after begin time"));
            }
        }
    }
    ,
    /**
     * Fetches the assignments for the current session.
     * @param {Object} frm - The current form object.
     */
    fetch_assignments(frm) {
        frappe.db.get_list("Topic Assignment", {
            filters: {
                docstatus: 0,
                council: cur_frm.doc.council,
                status: "Accepted"
            }
        }).then((assignments) => {
            // Clear any existing assignments in the child table:
            frm.doc.assignments = '';
            // Loop through the assignments and add them to the child table:
            assignments.forEach(assignment => {
                frm.add_child('assignments', {
                    topic_assignment: assignment.name,
                });
            });
            // Refresh the child table to display assignments:
            frm.refresh_field('assignments');
        });
    }
});
frappe.ui.form.on("Session Topic Assignment", {
    topic_assignment: function (frm, cdt, cdn) {
        // Get the current row
        let row = locals[cdt][cdn];
        // Call the check_assignment_duplicate function to check for duplicate assignments
        check_assignment_duplicate(frm, row);
        frappe.db.get_value("Topic Assignment", row.topic_assignment, ["title", "description"], (assignment) => {
            if (assignment) {
                let title = assignment.title
                let description = assignment.description
                frappe.model.set_value(cdt, cdn, 'title', title);
                frappe.model.set_value(cdt, cdn, 'description', description);

            }
        });
        frm.refresh_field('assignments');
    },
});
frappe.ui.form.on("Session Member", {
    employee: function (frm, cdt, cdn) {
        // Get the current row
        let row = locals[cdt][cdn];
        frappe.db.get_value("Employee", row.employee, "employee_name", (employee) => {
            if (employee) {
                let member_name = employee.employee_name
                frappe.model.set_value(cdt, cdn, 'member_name', member_name);
                academia.councils.utils.check_member_duplicate(frm, row);
            }
        });

        frm.refresh_field('members');
    },
    member_role: function (frm, cdt, cdn) {
        // Get the current row
        let row = locals[cdt][cdn];
        // Call the check_council_head_and_reporter_duplication function to check for duplicate members Council Heads and Reporters
        academia.councils.utils.check_council_head_and_reporter_duplication(frm, row);
    },
});
// Function to check for duplicate assignments
check_assignment_duplicate = function (frm, row) {
    // Iterate through each member in the form's assignments field
    frm.doc.assignments.forEach((assignment) => {
        // Check if the current row's topic_assignment is not empty or the same as the current assignment being iterated
        if (!(row.topic_assignment == "" || row.idx == assignment.idx)) {
            // Check if the current row's topic_assignment is the same as the assignment's topic_assignment
            if (row.topic_assignment == assignment.topic_assignment) {
                // Clear the topic_assignment value in the current row
                row.topic_assignment = "";
                // Refresh the assignments field in the form to reflect the changes
                frm.refresh_field("assignments");
                // message indicating that the topic_assignment already exists in a specific row
                msgprint(
                    __(`${row.topic_assignment} already exists in row ${assignment.idx}`)
                );
                // stop loop
                return;
            }
        }
    });
};