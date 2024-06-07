// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transaction', {

    refresh: function(frm) {

        // frappe.call({
        //     method: 'frappe.client.get_list',
        //     args: {
        //         doctype: 'Employee',
        //         filters: {
        //             designation: frm.doc.recipient_designation,
        //             company: frm.doc.company,
        //         },
        //         fields: ['user_id']
        //     },
        //     callback: function(response) {
                
        //         recipients = response.message
        //         console.log(recipients.length)

        //         recipients.forEach(function(recipient) {
        //             console.log(recipient)
        //             // Create a new row in the multiselect table field
        //             // var row = frm.add_child('recipient_multi_select_table');
        //             // row.recipient = recipient.user_id;
        //         });
        //         // Refresh the table to display the new rows
        //         // frm.refresh_field('recipient_multi_select_table');

        //     }
        // });
        
        if(frm.doc.docstatus === 1)       
        {
            // // unhide the actions table after submit
            // frm.set_df_property("related_to_table","hidden",0);
            // frm.refresh_fields();  

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
                            
                            console.log(last_action);
                            // show actions if the user is the last redirected
                            if(last_action && last_action.type === "Redirected" && last_action.redirected_to === frappe.session.user) {
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

        // frm.fields_dict['sub_external_entity'].get_query = function(doc) {
        //     return {
        //         filters: {
        //             'parent_external_entity':doc.externalEntity
        //         }
        //     };
        // };
       

    },

    // Advance Get members Dialog
    get_recipients: function (frm) {
        
    let d=new frappe.ui.form.MultiSelectDialog({
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
        // var prompt_company;
        // var prompt_designation;
        // var prompt_department;

        // frappe.prompt([
        //     {
        //         fieldname: 'company',
        //         label: __('Company'),
        //         fieldtype: 'Link',
        //         options: 'Company',
        //         hidden: function () {
        //             return frm.doc.transaction_scope === "In Company";
        //         },
        //         reqd: function () {
        //             return frm.doc.transaction_scope === "In Company";
        //         },
        //         onchange: function () {
        //             prompt_company = this.value
        //         }
        //     },
        //     {
        //         fieldname: 'to_party',
        //         label: __('To Party'),
        //         fieldtype: 'Select',
        //         options: ['Department', 'External Entity'],
        //         hidden: true,
        //         default: function () {
        //             if(frm.doc.transaction_scope === "With External Entity")
        //                 return 'External Entity'
        //             else
        //                 return 'Department'
        //         }
        //     },
        //     {
        //         fieldname: 'to_department',
        //         label: __('To Department'),
        //         fieldtype: 'Dynamic Link',
        //         options: 'to_party',
        //         // reqd: 1
        //         get_query: function() {
        //             return {
        //                 filters: {
        //                     company: prompt_company
        //                 }
        //             };
        //         },
        //         onchange: function () {
        //             prompt_department = this.value
        //         }
        //     },
        //     {
        //         fieldname: 'designation',
        //         label: __('Designation'),
        //         fieldtype: 'Link',
        //         options: 'Designation',
        //         // reqd: 1,
        //         onchange: function () {
        //             prompt_designation = this.value
        //         }
        //     },
        //     {
        //         fieldname: 'redirected_to',
        //         label: __('Redirected To'),
        //         fieldtype: 'Link',
        //         options: 'User',
        //         // reqd: 1,
                
        //     },
        //     {
        //         fieldname: 'details',
        //         label: __('Details'),
        //         fieldtype: 'Text',
        //         reqd: 0,
        //     }
        // ], function(values) {
        //     var childTable = cur_frm.add_child('actions');

        //     childTable.to_party = values.to_party;
        //     childTable.to_department = values.to_department;
        //     childTable.action_date = frappe.datetime.now_datetime();
        //     childTable.created_by = frappe.session.user;
        //     childTable.type = "Redirected";
        //     childTable.details = values.details;

        //     // Fetch the user associated with the selected designation
        //     frappe.model.with_doc('User', values.redirected_to, function() {
        //         var user = frappe.model.get_doc('User', values.redirected_to);
        //         if (user) {
        //             childTable.redirected_to = user.name;
                    
        //             // update share permission for the current user so he cant share more than one time
        //             // this not work for the owner
        //             frappe.call({
        //                 method: "academia.transaction_management.doctype.transaction.transaction.update_share_permissions",
        //                    args: {
        //                     docname: frm.doc.name,
        //                     user: frappe.session.user,
        //                     permissions:{
        //                         "read": 1,
        //                         "write": 0,
        //                         "share": 0,
        //                         "submit":0
        //                     },
        //                 },
        //                 callback: function(response) {
        //                     if (response && response.message) {
        //                         console.log(response.message);
        //                     }
        //                 },
        //             });
        //             frappe.call({
        //                 method: "frappe.share.add",
        //                 args: {
        //                     doctype: "Transaction",
        //                     name: frm.doc.name,
        //                     user: user.name,
        //                     read: 1,
        //                     write: 1,
        //                     share: 1,
        //                     submit:1,
        //                     everyone: 0
        //                 },
        //                 callback:function(response){
        //                     if(response.message) {
        //                         console.log(response.message);
        //                     }
        //                 }
        //             });

        //             frappe.call({
        //                 method: "frappe.client.save",
        //                 args: {
        //                     doc: frm.doc
        //                 },
        //                 callback: function(response) {
        //                     if (response && response.message) {
        //                         location.reload();
        //                         frappe.msgprint(response.message);
        //                     }
        //                 }
        //             });


        //             // Fetch the user associated with the selected designation
        //             frappe.call({
        //                 method: "frappe.client.get_value",
        //                 args: {
        //                     doctype: "Employee",
        //                     fieldname: "user_id",
        //                     filters: {
        //                         designation: values.designation,
        //                         company: values.company
        //                     }
        //                 },
        //                 callback: function(response) {
        //                     if (response && response.message && response.message.user_id) {
        //                         childTable.redirected_to = response.message.user_id;
        //                         // Save the document
        //                         frappe.call({
        //                             method: "frappe.client.save",
        //                             args: {
        //                                 doc: frm.doc
        //                             },
        //                             callback: function(saveResponse) {
        //                                 if (saveResponse && saveResponse.message) {
        //                                     location.reload();
        //                                 }
        //                                 frappe.msgprint(saveResponse.message);
        //                             }
        //                         });
        //                     } else {
        //                         frappe.msgprint("No user found for the selected designation in the specified company.");
        //                     }
        //                 }
        //             });
        //         }
        //     });
        // }, __('Redirect Transaction'));
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
                    console.log(r.exc);
                    if(r.message) {
                        console.log(r.message);
                        frm.set_value('status', 'Approved');
                        // location.reload();   
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
                    if(!r.exc) {
                        frappe.msgprint(__("New document created in Transaction Action"));
                        
                        frm.set_value("status", "Rejected");
                        frm.save(function() {
                            frm.refresh();
                        });
                    }
                }
            });
        }, __('Enter Rejection Details'), __('Submit'));
    });
}
