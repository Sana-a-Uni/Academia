// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Council", {
  validate: function (frm) {
    academia.councils.utils.validate_head_exist(frm.doc.members);
  },
});

frappe.ui.form.on("Council Member", {
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
