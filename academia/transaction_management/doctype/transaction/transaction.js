// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transaction', {
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
  },


  // onload:
  // function(frm) {
  //  if(frm.doc.docstatus === 0)
  //    {

  //      // if user is admin ignore bcoz he cant be employee
  //      if(frappe.session.user !== "Administrator")
  //      {
  //        // Fetch the current employee's document only if the docstatus is draft
  //        frappe.call({
  //          method: 'frappe.client.get_value',
  //          args: {
  //            doctype: 'User',
  //            filters: { name: frappe.session.user },
  //            fieldname: 'email'
  //          },
  //          callback: function(response) {
  //            if (response.message && response.message.email) {
  //              var userEmail = response.message.email;

  //              frappe.call({
  //                method: 'frappe.client.get',
  //                args: {
  //                  doctype: 'Employee',
  //                  filters: { user_id: userEmail }
  //                },
  //                callback: function(response) {
  //                  if (response.message) {
  //                    var employee = response.message;
  //                    // Set the default value of the department field to the current employee's department
  //                    frm.set_value('department', employee.department);
  //                    frm.set_value('designation', employee.designation);
  //                    // You can access other fields of the employee document as well
  //                    // Example: frm.set_value('employee_name', employee.employee_name);
  //                  }
                   
  //                }
  //              });
  //            }  
  //          }
  //        }); 
  //      }
  //    }
  //  },

    refresh: function(frm) {

        if(frm.doc.docstatus === 1)       
        {
            if(!frm.doc.__islocal )
            {
                frappe.call({
                    method: "academia.transaction_management.doctype.transaction_action.transaction_action.get_transaction_actions",
                    args: {
                        transaction_name: frm.doc.name
                    },
                    callback: function(r) {
                        if(r.message[0]) {
                            
                            var last_action = r.message[0];
                            // console.log(last_action);
                            if(
                                last_action
                                // && last_action.type === "Redirected" 
                                // && last_action.recipients.split(',')
                                //                          .map(recipient => recipient.trim())
                                //                          .includes(String(frappe.session.user))
                            ) {
                                add_approve_action(frm);
                                add_redirect_action(frm);
                                add_reject_action(frm);
                                add_council_action(frm);
                            }  
                        }
                        // show actions if the user is one of the recipients
                        else if(frm.doc.recipients.some(row => row.recipient_email === frappe.session.user))
                        {   
                            add_approve_action(frm);
                            add_redirect_action(frm);
                            add_reject_action(frm);
                            add_council_action(frm);
                        } 
                    }
                });  
            }
         
        }

        // Set query for category field
        frm.set_query('category', function() {
            return {
                filters: {
                    'is_group': 1,
                }
            };
        });
        // Filter the External Entity options based on is_group field
        frm.set_query('main_external_entity', function() {
            return {
              filters: {
                is_group: 1
              }
            };
          });


        // Set query for sub_category field based on selected category
        frm.fields_dict['sub_category'].get_query = function(doc) {
            return {
                filters: {
                    'parent_category': doc.category
                }
            };
        };

        frm.fields_dict['sub_external_entity'].get_query = function(doc) {
            return {
                filters: {
                    'parent_external_entity':doc.externalEntity
                }
            };
        };
       

    },


    // refresh action html template only when press this button
    refresh_button:function (frm) {

      frappe.call({
        method: "academia.transaction_management.doctype.transaction.transaction.get_actions_html",
        args: {
            transaction_name: frm.doc.name
            },
        callback: function(r) {
            if(r.message) {
                frm.set_df_property("actions", "options", r.message);
                // console.log(r.message);
            }
        }
        });
    },

    main_external_entity:function(frm){

      var main_entity=frm.doc.main_external_entity
      // frappe.msgprint("here")
     // Filter the External Entity options based on is_group field
     frm.set_query('sub_external_entity', function() {
      return {
        filters: {
          parent_external_entity: main_entity
        }
      };
    });

   
      
      frm.set_query("external_entity_designation", function (doc, cdt, cdn) {
        return {
          "filters": {
            "parent": main_entity
          },
        };
      });
      
  
  },
  sub_external_entity:function(frm){

    var sub_entity=frm.doc.sub_external_entity
    // frappe.msgprint("here")
   // Filter the External Entity options based on is_group field
    
    
    frm.set_query("external_entity_designation", function (doc, cdt, cdn) {
      return {
        "filters": {
          "parent": sub_entity
        },
      };
    });
    



},
    // Advance Get members Dialog
    get_recipients: function (frm) {

      var all_companies = frm.doc.transaction_scope === "Among Companies";
      var setters = {
        employee_name: null,
        department: null,
        designation: null
      };
  
      if (all_companies) {
        setters.company = null;
      }
  
      let d=new frappe.ui.form.MultiSelectDialog({
        doctype: "Employee",
        target: frm,
        setters: setters,
  
        // add_filters_group: 1,
        date_field: "transaction_date",
  
        get_query() {
          if (all_companies) {
            // frappe.msgprint("all")
            return {
              filters: { docstatus: ['!=', 2] }
            };
          } else {
            // frappe.msgprint("not all")
            return {
              filters: { docstatus: ['!=', 2], company: frm.doc.company }
          }}
        },
  
        primary_action_label: "Get Recipients",
        action(selections) {
        console.log(selections)
  
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
            console.log(selectedEmployees);
            // emptying 
  
            frm.set_value('recipients', []);
  
            selectedEmployees.forEach((employee) => {
  
              frm.add_child("recipients", {
                // employee: recipient,
                recipient_name:employee.employee,
                recipient_company:employee.company,
                recipient_department:employee.department,
                recipient_designation:employee.designation,
                recipient_email:employee.user_id,
                // member_name: employee.employee_name,
                // member_role: "Council Member"
              })
            })
  
            this.dialog.hide();
  
            frm.refresh_field("recipients");
          }
        });
        }
      });
    },

    sub_category: function(frm) {

      // Clear previously added attach image fields
      frm.clear_table("attachments");

      // Fetch Transaction Type Requirements based on the selected Transaction Type
      if (frm.doc.sub_category) {
        frappe.call({
          method: "academia.transaction_management.doctype.transaction.transaction.get_transaction_category_requirement",
          args: {
            transaction_category: frm.doc.sub_category
          },
          callback: function(response) {
            // Add attach image fields for each Transaction Type Requirement
            const requirements = response.message || [];

            requirements.forEach(function(requirement) {
              const fieldname =  requirement.name.replace(/ /g, "_").toLowerCase()+"_file";
              frm.add_child("attachments", {
                attachment_name: fieldname,
                attachment_label: requirement.name,
                fieldtype: "Attach Image",
                required: requirement.required,
              });
            });

            // Hide 'add row' button
            frm.get_field("attachments").grid.cannot_add_rows = true;
            // Stop 'add below' & 'add above' options
            frm.get_field("attachments").grid.only_sortable();
            //make the lables uneditable
            frm.fields_dict.attachments.grid.docfields[1].read_only = 1;

            // Refresh the form to display the newly added fields
             frm.refresh_fields("attachments");
          }
        });
      }
    },

   // Validate function
   before_save: function(frm) {
    // Check if any required attachment is missing
    let missing_attachments = [];
    if (frm.doc.attachments && frm.doc.attachments.length > 0) {
        frm.doc.attachments.forEach(attachment => {
            if (attachment.required && !attachment.file) {
                missing_attachments.push(attachment.attachment_label);
            }
        });
    }

    if (missing_attachments.length > 0) {
        let message =` Please attach the following required files before saving:\n\n${missing_attachments.join('\n')}`;
        frappe.throw(message);
    }}
});


function add_redirect_action(frm) {
    cur_frm.page.add_action_item(__('Redirect'), function() {
        frappe.new_doc('Transaction Action', {
            'transaction': frm.doc.name,
            'type': 'Redirected',
            'from_company': frm.doc.company,
            'from_department':frm.doc.department,
            'from_designation': frm.doc.designation,

        });
         // back to Transaction after save the transaction action
         frappe.ui.form.on("Transaction Action", {
            on_submit: function(frm) {
                frappe.set_route('Form', 'Transaction', frm.doc.transaction);
                location.reload();
            },
        })
    });
}

function add_council_action(frm) {
    cur_frm.page.add_action_item(__('Council'), function() {
        });
}

function add_approve_action(frm) {
    cur_frm.page.add_action_item(__('Approve'), function() {
        frappe.prompt([
            {
                label: 'Details',
                fieldname: 'details',
                fieldtype: 'Text',
            }
        ], function(values) {
            frappe.call({
                method: "academia.transaction_management.doctype.transaction.transaction.create_new_transaction_action",
                args: {
                    user_id: frappe.session.user,
                    transaction_name: frm.doc.name,
                    type: "Approved",
                    details: values.details || "",
                },
                callback: function(r) {
                    if(r.message) {
                        // frm.set_value('status', 'Approved');
                        frappe.db.set_value('Transaction', frm.docname, 'status', 'Approved');

                        // frm.save(function() {
                        //     // location.reload();   
                        // });                    
                        }
                }
            });
        }, __('Enter Approval Details'), __('Submit'));
        
    });
}

function add_reject_action(frm) {
    cur_frm.page.add_action_item(__('Reject'), function() {
        frappe.prompt([
            {
                label: 'Details',
                fieldname: 'details',
                fieldtype: 'Text',
            }
        ], function(values) {
            frappe.call({
                method: "academia.transaction_management.doctype.transaction.transaction.create_new_transaction_action",
                args: {
                    user_id: frappe.session.user,
                    transaction_name: frm.doc.name,
                    type: "Rejected",
                    details: values.details || "",
                },
                callback: function(r) {
                    if(r.message) {
                        frappe.db.set_value('Transaction', frm.docname, 'status', 'Rejected');
                    }
                }
            });
        }, __('Enter Rejection Details'), __('Submit'));
    });
}
