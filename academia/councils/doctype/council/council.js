// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Council", {
  // Setup function called when the Council form is loaded
  setup: function (frm) {
    // Changing Button Style
    $(`<style>
      .btn[data-fieldname="get_members"] {
        background-color: #171717; /* Custom dark gray */
        color: white;
      }
      .btn[data-fieldname="get_members"]:hover {
        background-color: #171710 !important;/* Slightly darker gray for interaction states */
        color: white !important;
      }
        </style>`).appendTo("head");
  },

  // validate: function (frm) {
  //   academia.councils.utils.validate_head_exist(frm.doc.members);
  // },

  // Filtering administrative body based on the Company
  company: function (frm) {
    frm.set_query("administrative_body", function () {
      return { "filters": [["Department", "company", "=", frm.doc.company]] };
    });
    frm.set_query("employee", "members", function () {
      if (frm.doc.get_members_from_other_companies == 0) {
        return { filters: { "company": frm.doc.company } };
      } else {
        // Return an empty filter object
        return {};
      }
    });
  },

  administrative_body: function (frm) {
    frm.events.check_if_administrative_body_already_has_council(frm);


  },
  check_if_administrative_body_already_has_council(frm) {
    frappe.db.get_list('Council', {
      fields: ['name'],
      filters: {
        administrative_body: frm.doc.administrative_body
      }
    }).then(records => {
      if (records && records.length > 0) {
        msgprint(__(`This Administrative body already has a Council`)); // views a message to user
        frm.doc.administrative_body = "";
        frm.refresh_field("administrative_body");
        throw __(`This Administrative body already has a Council`);
      }
    })

  },

  // Filltering by company
  get_members_from_other_companies: function (frm) {
    frm.refresh_field("company");
    console.log(frm.doc.get_members_from_other_companies);
  },

  // Advance Get members Dialog
  get_members: function (frm) {
    new frappe.ui.form.MultiSelectDialog({
      doctype: "Employee",
      target: frm,
      setters: {
        employee_name: null,
        company: frm.doc.company,
        department: frm.doc.administrative_body,
        designation: null
      },
      // add_filters_group: 1,
      date_field: "transaction_date",
      get_query() {
        return {
          filters: { docstatus: ['!=', 2], company: this.setters.company }
        }
      },
      primary_action_label: "Get Members",
      action(selections) {
        // console.log(d.dialog.get_value("company"));
        // emptying Council members
        frm.set_value('members', []);
        // Hold employee names 
        selections.forEach((member, index, array) => {
          frappe.db.get_value("Employee", member, "employee_name", (employee) => {
            if (employee) {
              frm.add_child("members", {
                employee: member,
                member_name: employee.employee_name,
                member_role: "Council Member"
              })
              // Refreshing the Council Members in the last itration
              console.log(`array => ${array}`)
              if (index === array.length - 1) {
                frm.refresh_field("members");
              }
            }
          });
        });
        this.dialog.hide();
      }
    });

  }


});

/*
 * locals => is an a list that gets curent doc type
 * cdt is Child DocType name i.e Council Member
 * cdn is the row name for e.g bbfcb8da6a
 */
frappe.ui.form.on("Council Member", {
  // Event triggered when the employee field changes in the Council Member form
  employee: function (frm, cdt, cdn) {
    // Get the current row
    let row = locals[cdt][cdn];
    // Call the check_member_duplicate function to check for duplicate members
    // View 
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

