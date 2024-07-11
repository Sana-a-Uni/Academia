// Copyright (c) 2024, SanU Development Team and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transaction Category', {
    setup: function (frm) {
        // Changing Button Style
        $(`<style>
          .btn[data-fieldname="get_recipients"] {
            background-color: #171717; /* Custom dark gray */
            color: white;
          }
          .btn[data-fieldname="get_recipients"]:hover {
            background-color: #171710 !important;/* Slightly darker gray for interaction states */
            color: white !important;
          }
          
          .btn[data-fieldname="refresh_button"] {
            background-color: #171717; /* Custom dark gray */
            color: white;
          }
          .btn[data-fieldname="refresh_button"]:hover {
            background-color: #171710 !important;/* Slightly darker gray for interaction states */
            color: white !important;
          }
            </style>`).appendTo("head");


        // Hide 'add row' button
        frm.get_field("recipients").grid.cannot_add_rows = true;
        // Stop 'add below' & 'add above' options
        frm.get_field("recipients").grid.only_sortable();
        frm.refresh_field("recipients");
      },
      
    refresh: function(frm) {
        // Filter the "Parent Transaction Category" field choices
        frm.fields_dict['parent_category'].get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ["Transaction Category", "is_group", "=", 1],
                    ['Transaction Category', 'parent_category', '=', ''],  // Only show parties without a parent
                    // ['Transaction Category', 'name', '!=', doc.name]  // Exclude the current item
                ]
            };
        };
    },

    // validate: function(frm) {
    //     // Validation for is_group checkbox
    //     if (frm.doc.is_group) {
    //         // If is_group is checked, clear the parent_category field
    //         frm.set_value('parent_category', null);
    //         frm.refresh_field('parent_category');
    //     } else {
    //         // If is_group is not checked, ensure parent_category is not empty
    //         if (!frm.doc.parent_category) {
    //             frappe.throw(__("Parent Category is mandatory if 'Is Group' is not checked."));
    //         }
    //     }
    // },
    
    // Advance Get members Dialog
    get_recipients: function (frm) {

        var setters = {
          employee_name: null,
          department: null,
          designation: null,
          company: null,
        };
  
        let existingRecipients = frm.doc.recipients || [];
        let existingRecipientIds = existingRecipients.map(r => r.recipient_email);

        let d=new frappe.ui.form.MultiSelectDialog({
          doctype: "Employee",
          target: frm,
          setters: setters,
    
          // add_filters_group: 1,
          date_field: "transaction_date",
    
          get_query() {
            let filters = {
              docstatus: ['!=', 2],
              department: ['!=', null],
              designation: ['!=', null],
              user_id: ['not in', existingRecipientIds], // don't show Employee of current user
            };
            
            return {
              filters: filters
            };
          },
    
          primary_action_label: "Get Recipients",
          action(selections) {
  
          // Fetch the selected employees with specific fields
          frappe.call({
              method: "frappe.client.get_list",
              args: {
              doctype: "Employee",
              filters: { name: ["in", selections] },
              fields: ["employee_name", "designation", "department", "company", "user_id"]
            },
            callback: (response) => {
              var selectedEmployees = response.message;
 
              selectedEmployees.forEach((employee) => {
                frm.add_child("recipients", {
                  recipient_name:employee.employee_name,
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
  
      clear_recipients: function(frm) {
        frm.clear_table("recipients");
        frm.refresh_field("recipients");
      },

});
