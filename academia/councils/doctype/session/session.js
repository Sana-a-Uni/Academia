// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Session", {
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
                        faculty_member: council_member.faculty_member,
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
