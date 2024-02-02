// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
frappe.ui.form.on("Session", {
    setup: function (frm) {
        // method to fetch members from a council document
        frm.fetch_members_from_council = function (council_docname) {
            // call get_linked_council method from python api to get linked council
            frm.call('get_linked_council', { docname: council_docname })
                .then(r => {
                    // Check if the method returned a value
                    if (r.message) {
                        // set linked council that returned 
                        let linked_doc = r.message;
                        // Clear existing members
                        frm.doc.members = '';
                        council_members = linked_doc.members;
                        council_members.forEach(council_member => {
                            // Add each council member to session members
                            frm.add_child('members', {
                                faculty_member: council_member.faculty_member,
                                attendance: "Attend",
                                member_role: council_member.member_role
                            });
                            // Refresh the 'members' field
                            frm.refresh_field('members');
                        });
                    }
                });
        }
    },
    council(frm) {
        // Event handler for 'council' field change
        if (frm.doc.council) {
            // Fetch members from the selected council
            frm.fetch_members_from_council(frm.doc.council);
        }
    }
    ,
    // Fetches assignments from the server and populates the 'assignments' child table.
    fetch_assignments(frm) {
        // Call the server-side 'get_assignments' method to retrieve assignments:
        frm.call('get_assignments', { council: frm.doc.council })
            .then(r => {
                // If assignments are received successfully:
                if (r.message) {
                    const assignments = r.message;

                    // Clear any existing assignments in the child table:
                    frm.doc.assignments = '';

                    // Create child table rows for each assignment:
                    assignments.forEach(assignment => {
                        frm.add_child('assignments', {
                            topic_assignment: assignment.name,
                        });

                        // Refresh the child table to display the new rows:
                        frm.refresh_field('assignments');
                    });
                }
            });
    }
});