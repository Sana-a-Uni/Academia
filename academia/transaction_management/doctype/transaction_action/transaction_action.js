// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction Action", {
    onload: function(frm) {
    //     // Set the initial visibility of the to_section
    //     frm.toggle_display("to_section", frm.doc.type === "Redirected");

    },
    // type: function(frm) {
    //     // Toggle the visibility of the to_section when the type changes
    //     frm.toggle_display("to_section", frm.doc.type === "Redirected");
    // },
    transaction: function (frm) {
        // if(frm.doc.transaction)
        //     // console.log(frm.doc.transaction);
        // frappe.call({
        //     method: "frappe.client.get_list",
        //     args: {
        //       doctype: "Transaction",
        //       filters: { 
        //             name: frm.doc.transaction , 
        //         },
        //       fields: [
        //         "transaction_scope", 
        //         "company",
        //         "department", 
        //         "designation", 
        //     ]
        //     },
        //     callback: (response) => {
        //         var main_transaction = response.message
        //     }
        // });
    },

    // Advance Get members Dialog
    get_recipients: function (frm) {
        new frappe.ui.form.MultiSelectDialog({
          doctype: "Employee",
          target: frm,
          setters: {
            employee_name: null,
            company: null,
            department:  null,
            designation: null,
          },
          get_query() {
            return {
                filters: { 
                    docstatus: ['!=', 2],
                    company: this.setters.company,
                }
            }
          },
          primary_action_label: "Get Recipients",
          action(selections) {
             // Fetch the selected employees with specific fields
        frappe.call({
            method: "frappe.client.get_list",
            args: {
              doctype: "Employee",
              filters: { name: ["in", selections] },
              fields: ["name","employee", "designation", "department", "company", "user_id"]
            },
            callback: (response) => {
              var selectedEmployees = response.message;
    
              frm.set_value('recipients', []);
    
              selectedEmployees.forEach((employee) => {
    
                    frm.add_child("recipients", {
                    recipient_name:employee.employee,
                    recipient_company:employee.company,
                    recipient_department:employee.department,
                    recipient_designation:employee.designation,
                    recipient_email:employee.user_id,
                  })
    
              })
                this.dialog.hide();
              frm.refresh_field("recipients");
            }
          });
          }
        });
    
      },
    
});