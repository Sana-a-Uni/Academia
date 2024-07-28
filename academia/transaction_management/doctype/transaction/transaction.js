// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

let mustInclude = [];

var global_print_papaer = null;
var global_is_received = null;
var global_action_name = null;
var global_recipient_docname = null;  

frappe.ui.form.on('Transaction', {
  setup: function (frm){
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

  onload: function(frm){
    if(frm.doc.docstatus === 1){
      if (frm.doc.status === "Completed") {
        $(".btn-secondary").filter(function() {
          return $(this).text().trim() === "Cancel";
        }).hide();
      }
  
      frappe.call({
        method: "academia.transaction_management.doctype.transaction.transaction.is_there_approve_or_reject_acions",
        args: {
            docname: frm.doc.name
        },
        callback: function(r) {
            if(r.message) {
              if (r.message) {
                $(".btn-secondary").filter(function() {
                  return $(this).text().trim() === "Cancel";
                }).hide();
              }   
            }
          }
      });
    }

   if(frm.doc.docstatus === 0)
     {
      global_print_papaer = null;
      global_is_received = null;
      global_action_name = null;
      global_recipient_docname = null;

      frm.set_value('status', "Pending");


       // if user is admin ignore bcoz he cant be employee
       if(frappe.session.user !== "Administrator")
       {
         // Fetch the current employee's document only if the docstatus is draft
         frappe.call({
           method: 'frappe.client.get_value',
           args: {
             doctype: 'User',
             filters: { name: frappe.session.user },
             fieldname: 'email'
           },
           callback: function(response) {
             if (response.message && response.message.email) {
               var userEmail = response.message.email;

               frappe.call({
                 method: 'frappe.client.get',
                 args: {
                   doctype: 'Employee',
                   filters: { user_id: userEmail }
                 },
                 callback: function(response) {
                   if (response.message) {
                     var employee = response.message;
                     // Set the default value of the department field to the current employee's department
                     frm.set_value('department', employee.department);
                     frm.set_value('designation', employee.designation);
                     // You can access other fields of the employee document as well
                     // Example: frm.set_value('employee_name', employee.employee_name);
                   }
                   
                 }
               });
             }  
           }
         }); 
       }
     }
   },

  refresh: function(frm){
    global_print_papaer = null;
    global_is_received = null;
    global_action_name = null;
    global_recipient_docname = null;

    frm.fields_dict.recipients.grid.wrapper.find(".grid-add-row")
    .toggle(!frm.doc.through_route);

    // Disable the "Add New" button when through_route is checked
    frm.fields_dict.recipients.grid.wrapper.find(".grid-add-row")
      .prop("disabled", frm.doc.through_route);
      
    // Disable the "Get Recipients" button when through_route is checked and there is at least one recipient
    frm.set_df_property("get_recipients", "hidden", frm.doc.through_route && frm.doc.recipients.length > 0);
    frm.set_df_property("get_recipients", "disabled", frm.doc.through_route && frm.doc.recipients.length > 0);
      if(frm.doc.docstatus === 1)       
      {
          // Closed Button
          if(frappe.user_roles.includes("Transaction Manager") && frm.doc.status !== 'Closed'){
            frm.add_custom_button("Closed", () => {

                const share_name = frm.doc.name;
                console.log("Pressed:", share_name)

                // Call the Python function to get the shared users
                frappe.call({
                    method: "academia.transaction_management.doctype.transaction.transaction.update_closed_premissions",
                    args: {
                      docname: share_name,
                    },
                    callback: function(r) {
                      if(r.message){

                        location.reload();
                      }
                    }
                });
            })
          }

          if (!frm.doc.__islocal) {
            frappe.call({
              method: "academia.transaction_management.doctype.transaction.transaction.search_in_actions_for_print_paper_user",
              args: {
                transacion_name: frm.doc.name,
                user: frappe.session.user,
                from_company: frm.doc.start_with_company??'',
                from_department: frm.doc.start_with_department??'',
                from_designation: frm.doc.start_with_designation??''
              },
              callback: function(r) {
                if (r.message) {
                  console.log(r.message);
                  msg = r.message;
                 if(msg[0]){
                  global_action_name = msg[0];
                 }
          
                  if (msg[1]) {
                    global_print_papaer = true;
                    console.log(msg[1]);
                  }
                  if (msg[2]) {
                    global_is_received = true;
                    console.log(msg[2]);
                  }
                  if(msg[3]){
                    console.log("receipent docname:", msg[3])
                    global_recipient_docname = msg[3];
                  }
          
                  // After the first method, call the get_user_permissions method
                  frappe.call({
                    method: "academia.transaction_management.doctype.transaction.transaction.get_user_permissions",
                    args: {
                      docname: frm.doc.name,
                      user: frappe.session.user
                    },
                    callback: function(response) {
                      var docshare = response.message;
                      if (docshare && docshare.share === 1 && frm.status != "Closed") {
                        
                        console.log("print_paper_checked2: ", global_print_papaer);
                        console.log("is_received2: ", global_is_received);
          
                        if (global_print_papaer && !global_is_received) {
                          add_received_action(frm);
                        } else if((global_print_papaer == true && global_is_received == true) || (global_print_papaer == null )){
                          add_approve_action(frm);
                          add_reject_action(frm);
                          if(!frm.doc.circular){
                            add_redirect_action(frm);
                            if(frappe.user_roles.includes("Council Head")){
                              frappe.call({
                                method: "academia.transaction_management.doctype.transaction.transaction.get_last_topic_action",
                                args: {
                                  docname: frm.doc.name
                                },
                                callback: function(r) {
                                  console.log("council action: ", r.message)  
                                    if(r.message) {
                                      add_council_action(frm);
                                    }
                                  }
                              });
                              
                            }
                          }
                        }
                      }
                    }
                  });
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
      
      // Set query for sub_category field based on selected category
      frm.fields_dict['sub_category'].get_query = function(doc) {
          return {
              filters: {
                  'parent_category': doc.category
              }
          };
      };

      // Filter the External Entity options based on is_group field
      frm.set_query('main_external_entity_from', function() {
        return {
          filters: {
            is_group: 1
          }
        };
      });

      frm.set_query('main_external_entity_to', function() {
        return {
          filters: {
            is_group: 1
          }
        };
      });

      frm.set_query('reference_transaction', function() {
        return {
          filters: {
            transaction_scope: "With External Entity",
            type:"Incoming",
            status: "Completed",
          }
        };
       });

      frm.doc.recipients.forEach(function(row) {
        if (frm.doc.full_electronic) {
          frm.doc.recipients.forEach(function(recipient) {
            frm.set_df_property("print_paper", "read_only", frm.doc.full_electronic, row.name);
            recipient.print_paper = 0;
          });
        }
      });

  },

  main_external_entity_from: function(frm){
    var main_entity=frm.doc.main_external_entity_from;
    console.log("here from");
    if(main_entity){
      frm.set_query('sub_external_entity_from', function() {
       return {
         filters: {
           parent_external_entity: main_entity
         }
       };
     });

     frm.set_query("external_entity_designation_from", function (doc, cdt, cdn) {
      return {
        "filters": {
          "external_entity": doc.main_entity
        },
        "ignore_permissions": true
      };
    });
    }
    else{
      frm.set_value("sub_external_entity_from", '');
      frm.set_value("external_entity_designation_from", '');
    }
  },


  main_external_entity_to: function(frm){
    var main_entity=frm.doc.main_external_entity_to;

    console.log("here to");
    if(main_entity){
      frm.set_query('sub_external_entity_to', function() {
       return {
         filters: {
           parent_external_entity: main_entity
         }
       };
      });

      frm.set_query("external_entity_designation_to", function (doc, cdt, cdn) {
       return {
         "filters": {
           "external_entity": main_entity
         },
       };
     });

    }
    
    else{
      frm.set_value("sub_external_entity_to", '');
      frm.set_value("external_entity_designation_to", '');
    }
  },

  through_route: function(frm){
    if (!frm.doc.sub_category)
    {
      update_must_include(frm)
    }
    if(frm.doc.through_route)
    {
      frm.doc.circular = false
      frm.refresh_field("circular");
    }
    frm.fields_dict.recipients.grid.wrapper.find(".grid-add-row")
      .prop("disabled", frm.doc.through_route);

    frm.set_df_property("get_recipients", "disabled", frm.doc.through_route && frm.doc.recipients.length > 0);
  },

  // refresh action html template only when press this button
  refresh_button: function(frm){

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
    }},
  
    // transaction_scope:function(frm){
    //   if (frm.doc.transaction_scope === "Among Companies") {
    //     // Set the 'through_route' field to checked and make it read-only
    //     frm.set_value("through_route", 1);
  
    //     frm.toggle_display("through_route", true);
    //     frm.toggle_reqd("through_route", true);
    //     frm.toggle_enable("through_route", false);
    //   } else {
    //     // Reset the 'through_route' field and make it editable
    //     frm.set_value("through_route", 0);
        
    //     frm.toggle_display("through_route", true);
    //     frm.toggle_reqd("through_route", false);
    //     frm.toggle_enable("through_route", true);
    //   }
    // },
  
    type:function(frm){
      if (frm.doc.type === "Incoming") {
        // if(frappe.session.user != "Administrator"){
          frappe.call({
            method: "academia.transaction_management.doctype.transaction.transaction.set_company_head",
            args: {
                user_id: frappe.session.user,
                company_of_creator: frm.doc.company
            },
            callback: function(r) {
                if(r.message) {
                  if (r.message) {
                    console.log(r.message.head_employee)
                    console.log("creation: ", frm.doc.created_by)
                    
                    frm.set_value('start_with', r.message.head_employee);
                    frm.set_df_property('start_with', 'hidden', 1);
                    frm.set_df_property('start_from_employee', 'hidden', 1);
                  }   
                }
              }
          });
          frm.toggle_display("through_route", true);
          frm.toggle_reqd("through_route", true);
          frm.toggle_enable("through_route", false);
        // }
        // else{
        //   console.log("It Is The Administrator")
        // }
      }
      else{
        frm.toggle_display("through_route", true);
        frm.toggle_reqd("through_route", false);
        frm.toggle_enable("through_route", true);
      }
    },
    
    start_with: function(frm) {
      console.log("Here Start With... ",frm.doc.start_with)
      if(frm.doc.start_with)
        {
          if (!frm.doc.sub_category)
          {
            update_must_include(frm)
          }
          frappe.call({
            method: "frappe.client.get",
            args: {
            doctype: "Employee",
            filters: { name: frm.doc.start_with },
            fields: ["designation", "department", "company"]
          },
          callback: (response) => {
              employee = response.message
              frm.set_value('start_with_company', employee.company);
              frm.set_value('start_with_department', employee.department);
              frm.set_value('start_with_designation', employee.designation);
            }
          });
        }
        else{
          frm.set_value('start_with_company', '');
          frm.set_value('start_with_department', '');
          frm.set_value('start_with_designation', '');
        }
        
    },
  
    circular: function (frm) {
      if (!frm.doc.sub_category)
      {
        update_must_include(frm)
      }
      if(frm.doc.circular)
      {
        frm.doc.through_route = false
        frm.refresh_field("through_route");
      }
  
    },

  get_default_template_button:function(frm){
    if (frm.doc.transaction_description && frm.doc.referenced_document) {
      frappe.confirm(
        __(
          "Are you sure you want to reload opening field?<br>All data in the field will be lost."
        ),
        function () {
          get_default_template(frm);
        }
      );
    }
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
    let existingRecipients = frm.doc.recipients || [];
    let existingRecipientIds = existingRecipients.map(r => r.recipient_email);
    // let filterCondition = "not in"
    // let filterValue = existingRecipientIds

    // TODO: also add start_with user_id to the exception
    // Add the current user to the existing recipient IDs
    existingRecipientIds.push(frappe.session.user);
    
    if(!frm.doc.circular && !frm.doc.sub_category && existingRecipients.length > 0){

      frappe.msgprint("You can select only one employee.");

      // // Disable the "Get Recipients" button
      // frm.get_field("get_recipients").df.read_only = true;
      // frm.refresh_field("get_recipients");

    }else{
      // Enable the "Get Recipients" button
      frm.get_field("get_recipients").df.read_only = false;
      frm.refresh_field("get_recipients");

      if (mustInclude.length > 0)
      {
        mustInclude = mustInclude.filter(item => !existingRecipientIds.includes(item));
        // filterCondition = "in"
        // filterValue = mustInclude
      }
          let d = new frappe.ui.form.MultiSelectDialog({
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
                user_id: ["in", mustInclude]
              };
    
          if (!all_companies) {
            filters.company = frm.doc.company;
          }
          
          return {
            filters: filters
          };
        },
  
        primary_action_label: "Get Recipients",
        action(selections) {

        // if the transaction through route you can select only one recipientS
        if (!frm.doc.circular && !frm.doc.sub_category && selections.length > 1) {
          frappe.msgprint("To Select Multi Recipients Make Circular Chickbox ON");
          return;
        }
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

            // // Check the value of the 'through_route' field
            // if (frm.doc.through_route) {
            //   // If 'through_route' is checked, only allow one recipient
            //   if (selectedEmployees.length > 1) {
            //     frappe.msgprint("You can only select one recipient when 'Through Route' is checked.");
            //     return;
            //   }
            // }

            // frm.set_value('recipients', []);
  
            selectedEmployees.forEach((employee) => {
              frm.add_child("recipients", {
                recipient_name:employee.employee_name,
                recipient_company:employee.company,
                recipient_department:employee.department,
                recipient_designation:employee.designation,
                recipient_email:employee.user_id,
                // print_paper: !frm.doc.full_electronic
              })
            })
  
            this.dialog.hide();
  
            frm.refresh_field("recipients");

            // Hide the "Add" button for the recipients table if through_route is checked and there's a recipient
            frm.get_field("recipients").grid.grid_buttons.find(".grid-add-row").toggle(!frm.doc.through_route || existingRecipients.length === 0);
          }
        });
        }
      });
    }
    
  },

  clear_recipients: function(frm) {
    frm.clear_table("recipients");
    frm.refresh_field("recipients");
  },

  referenced_document: function(frm) {
    get_default_template(frm);
  },

  sub_category: function(frm) {

    get_cateory_doctype(frm)

    // Clear previously added recipient fields
    frm.clear_table("recipients");
    frm.refresh_fields("recipients");

    // Fetch Transaction Type Recipients based on the selected category
    if (frm.doc.sub_category) {
      frappe.call({
        method: "academia.transaction_management.doctype.transaction.transaction.get_transaction_category_recipients",
        args: {
          transaction_category: frm.doc.sub_category
        },
        callback: function(response) {

          // Add recipient image fields for each Transaction Type Requirement
          const recipients = response.message || [];

          recipients.forEach(function(recipient) {
            frm.add_child("recipients", {
              recipient_name: recipient.recipient_name,
              step: recipient.step,
              recipient_company: recipient.recipient_company, 
              recipient_department: recipient.recipient_department, 
              recipient_designation: recipient.recipient_designation, 
              recipient_email: recipient.recipient_email,
              print_paper: recipient.print_paper,
              has_sign: recipient.has_sign,
            });
          });

          // Refresh the form to display the newly added fields
            frm.refresh_fields("recipients");
        }
      });
      
    // Clear previously added attach image fields
    frm.clear_table("attachments");

    // Fetch Transaction Type Requirements based on the selected Transaction Type
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
              // attachment_name: fieldname,
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

});


function add_redirect_action(frm) {
  cur_frm.page.add_action_item(__('Redirect'), function() {
      var is_received = false
      frm.doc.recipients.forEach(function(recipient) {
        if (recipient.recipient_email === frappe.session.user) {
          if (recipient.print_paper && recipient.is_received) {
            is_received = true
          }
        }
      });
      
        frappe.new_doc('Transaction Action', {
            'transaction': frm.doc.name,
            'type': 'Redirected',
            'from_company': frm.doc.start_with_company,
            'from_department':frm.doc.start_with_department,
            'from_designation': frm.doc.start_with_designation,
            'received': is_received,

        });
         // back to Transaction after save the transaction action
         frappe.ui.form.on("Transaction Action", {
          on_submit: function() {
            frappe.call({
              method: "academia.transaction_management.doctype.transaction.transaction.update_share_permissions",
              args: {
                docname: frm.doc.name,
                user: frappe.session.user,
                permissions: {
                  "read": 1,
                  "write": 0,
                  "share": 0,
                  "submit":0
              }
              },
              callback: function(response) {
                if(response.message)
                {
                    // back to Transaction after save the transaction action
                    frappe.set_route('Form', 'Transaction', frm.doc.name);
                    location.reload();
                    }
                  }
                });
            },
        })
    });
}

function add_council_action(frm) {
  cur_frm.page.add_action_item(__('Create Topic'), function() {

    frappe.call({
      method: "academia.transaction_management.doctype.transaction.transaction.create_new_transaction_action",
      args: {
          user_id: frappe.session.user,
          transaction_name: frm.doc.name,
          type: "Topic",
          details: "",
          transaction_scope: frm.doc.transaction_scope || ""
      },
      callback: function(r) {
          if(r.message) {
            // console.log(r.message);
            if (r.message) {
                location.reload();
            }
              // frappe.db.set_value('Transaction', frm.docname, 'status', 'Approved');     
            }
      }
  });

  });
}

function add_received_action(frm) {
  cur_frm.page.add_action_item(__('Received'), function() {

    // console.log(global_action_name)
    // console.log(global_print_papaer)
    // console.log(global_is_received)

      frappe.call({
      method: "academia.transaction_management.doctype.transaction.transaction.change_is_received_in_action_recipients",
      args: {
        rcipient_name: global_recipient_docname,
      },
      callback: function(r) {
        if (r.message) {
          location.reload();
          console.log(r.message)
        }
      },
      error: function(r) {
        frappe.show_alert({
          message: __("Error updating received status"),
          indicator: 'red'
        });
      }
    });
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
                    transaction_scope: frm.doc.transaction_scope || ""
                },
                callback: function(r) {
                    if(r.message) {
                      // console.log(r.message);
                      if (r.message) {
                          location.reload();
                      }
                        // frappe.db.set_value('Transaction', frm.docname, 'status', 'Approved');     
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
                    transaction_scope: frm.doc.transaction_scope || ""
                },
                callback: function(r) {
                    if(r.message) {
                        location.reload();
                        // frappe.db.set_value('Transaction', frm.docname, 'status', 'Rejected');
                    }
                }
            });
        }, __('Enter Rejection Details'), __('Submit'));
    });
}

function get_cateory_doctype(frm) {
  if (frm.doc.sub_category) {
    frappe.call({
      method: "academia.transaction_management.doctype.transaction.transaction.get_category_doctype",
      args: {
          sub_category: frm.doc.sub_category
      },
      callback: function(r) {
          if (r.message) {
              frm.set_value("referenced_doctype", r.message);
          }
      }
  });
  }else{
    frm.set_value("referenced_doctype", '');
    frm.set_value("referenced_document", '');
  }
}

function get_default_template(frm){

  if (frm.doc.referenced_doctype && frm.doc.referenced_document && frm.doc.sub_category) {
    frappe.call({
        method: "academia.transaction_management.doctype.transaction.transaction.render_template",
        args: {
            referenced_doctype: frm.doc.referenced_doctype,
            referenced_document: frm.doc.referenced_document,
            sub_category: frm.doc.sub_category,
        },
        callback: function(r) {
            if (r.message) {
                frm.set_value("transaction_description", r.message);
            } else {
                frappe.msgprint(__("Error rendering template"));
            }
        }
    });
  } else {
      frm.set_value("transaction_description", '');
  }

}

function update_must_include(frm) {
  if(frm.doc.start_with)
  {
    frm.clear_table("recipients");
    frm.refresh_field("recipients");

    if (frm.doc.transaction_scope === "Among Companies") {
      frappe.call({
        method: "academia.transaction_management.doctype.transaction.transaction.get_all_employees_except_start_with_company",
        args: {
          start_with_company: frm.doc.start_with_company
        },
        callback: function(response) {
          mustInclude = response.message;
        }
      });
    }
    else if(frm.doc.through_route){
      frappe.call({
        method: "academia.transaction_management.doctype.transaction.transaction.get_reports_hierarchy",
        args: {
          employee_name: frm.doc.start_with
        },
        callback: function(response) {
          
          mustInclude = response.message;
          
        }
      });
    }
      else {
        frappe.call({
          method: "academia.transaction_management.doctype.transaction.transaction.get_reports_hierarchy_reverse",
          args: {
            employee_name: frm.doc.start_with
          },
          callback: function(response) {
              mustInclude = response.message;
          }
        }); 
      }
  }
}