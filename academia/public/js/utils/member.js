frappe.provide("academia.councils.utils");
academia.councils.utils.check_member_duplicate = function (frm, row) {
	// Iterate through each member in the form's members field
	frm.doc.members.forEach((member) => {
		// Check if the current row's faculty_member is not empty or the same as the current member being iterated
		if (!(row.employee == "" || row.idx == member.idx)) {
			// Check if the current row's faculty_member is the same as the member's faculty_member
			if (row.employee == member.employee) {
				// message indicating that the member name already exists in a specific row
				msgprint(__("{0} already exists in row {1}", [row.member_name, member.idx]));
				// Clear the employee,member_name value in the current row
				row.employee = "";
				row.member_name = "";
				// Refresh the members field in the form to reflect the changes
				frm.refresh_field("members");
				// stop loop
				return;
			}
		}
	});
};
// Function to check Council Head or Reporter Duplication
academia.councils.utils.check_council_head_and_reporter_duplication = function (frm, row) {
	frm.doc.members.forEach((member) => {
		// Iterate through each member in the form's members field
		if (!(row.member_role == "" || row.idx == member.idx)) {
			// check if head or reporter is choosen and already existes
			if (
				(row.member_role == __("Council Head") &&
					member.member_role == __("Council Head")) ||
				(row.member_role == __("Council Reporter") &&
					member.member_role == __("Council Reporter"))
			) {
				// clears the felid
				row.member_role = "";
				// refresh changes
				frm.refresh_field("members");
				// message in decating that a Council head or Reporter exists
				msgprint(__("This Council already has a {0}", [member.member_role]));
				return;
			}
		}
	});
};
academia.councils.utils.validate_head_exist = function (members) {
	// Looping throw the members roles to check for a Council Head
	let filtered = members.filter((member) => member.member_role == __("Council Head"));

	// if a Council Head does not exist Throw an Exception
	if (!filtered) {
		frappe.throw(__(`This Council doesn't have a Council Head`)); // prevents saving the form by throwing an exception
	}
};
