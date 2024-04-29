// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Council", {
    // Setup function called when the Council form is loaded
    setup: function (frm) {
      // Function to check for duplicate members
      frm.check_member_duplicate = function (frm, row) {
        // Iterate through each member in the form's members field
        frm.doc.members.forEach((member) => {
          // Check if the current row's faculty_member is not empty or the same as the current member being iterated
          if (!(row.faculty_member == "" || row.idx == member.idx)) {
            // Check if the current row's faculty_member is the same as the member's faculty_member
            if (row.faculty_member == member.faculty_member) {
              // Clear the faculty_member value in the current row
              row.faculty_member = "";
              // Refresh the members field in the form to reflect the changes
              frm.refresh_field("members");
              // message indicating that the member name already exists in a specific row
              msgprint(
                __(`${row.member_name} already exists in row ${member.idx}`)
              );
              // stop loop
              return;
            }
          }
        });
      };
      // Function to check Council Head or Reporter Duplication
      frm.check_council_head_and_reporter_duplication = function (frm, row) {
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
              msgprint(__(`This Council already has a ${member.member_role}`));
              return;
            }
          }
        });
      };
    },
  
    // before_save is called when the form is saved
    before_save: function (frm) {
      // a flag to check if Council head exists
      let councilHeadExists = false;
      // Looping throw the members roles to check for a Council Head
      frm.doc.members.forEach((member) => {
        if (member.member_role == __("Council Head")) {
          councilHeadExists = true;
          return;
        }
      });
      // if a Council Head does not exist Throw an Exception
      if (!councilHeadExists) {
        msgprint(__(`This Council doesn't have a Council Head`)); // views a message to user
        throw __(`This Council doesn't have a Council Head`); // prevents saving the form by throwing an exception
      }
    },
  });
  
  /*
   * locals => is an a list that gets curent doc type
   * cdt is Child DocType name i.e Council Member
   * cdn is the row name for e.g bbfcb8da6a
   */
  frappe.ui.form.on("Council Member", {
    // Event triggered when the faculty_member field changes in the Council Member form
    faculty_member: function (frm, cdt, cdn) {
      // Get the current row
      let row = locals[cdt][cdn];
      // Call the check_member_duplicate function to check for duplicate members
      frm.check_member_duplicate(frm, row);
    },
    member_role: function (frm, cdt, cdn) {
      // Get the current row
      let row = locals[cdt][cdn];
      // Call the check_council_head_and_reporter_duplication function to check for duplicate members Council Heads and Reporters
      frm.check_council_head_and_reporter_duplication(frm, row);
    },
  });
  