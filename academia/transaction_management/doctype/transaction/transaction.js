// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

// frappe.listview_settings["Transaction"] = {
//     onload: function(listview) {

//         // Add filter for transactions created by the current user
//         listview.filter_list.add_filter("Transaction", "created_by", "=", frappe.session.user);

//         // Add filter for transactions redirected to the current user
//         listview.filter_list.add_filter("Transaction", "name", "in", frappe.db.get_all(
//             "Transaction Action",
//             filters={
//                 "redirected_to": frappe.session.user
//             },
//             pluck="main_transaction"
//         ));

//         // Refresh the listview to apply the filters
//         listview.refresh();
//     }
// };

frappe.listview_settings["Transaction"] = {
    get_list_context: function(context) {
        let user = frappe.session.user;
        let permitted_docs = frappe.get_permitted_documents(user, "Transaction", true);
        context.filters = {"name": ["in", permitted_docs]};
        return context;
    }
};

frappe.ui.form.on('Transaction', {
    
    onload: function(frm) {
        if (!frm.doc.start_date) {
            frm.set_value('start_date', frappe.datetime.get_datetime_as_string());
        }

    },
    refresh: function(frm) {
        //hide the actions table before submit
        if(frm.doc.docstatus != 1)       
            frm.set_df_property("actions_section", "hidden", 1);


        if(frm.doc.docstatus === 1 && !frm.doc.__islocal )
        {
            //frappe.msgprint("here")
            //frm.set_df_property("actions_section", "hidden", 0);
            
            // if there are actions
            if(frm.doc.actions.length !=0){

            // Get the last row of the actions child table
            var lastRow = frm.doc.actions.slice(-1)[0];

            // Retrieve the action type in the last row
            var last_action_type = lastRow.type;

            // Do something with the retrieved value
            frappe.msgprint(last_action_type);

            if(last_action_type == "Redirected")
                {
                    
                    add_recieve_action(frm)
                }

            else if(last_action_type == "Received")
                {
                    
        
                    add_approve_action(frm);
                    add_redirect_action(frm);
                    add_reject_action(frm)
                   
                }
                
            else if(response.message == "Canceld")//???spelling?
                    frappe.db.set_value('Transaction', frm.docname, 'status', 'Canceld');
            

            
            
                
            
           
        
        
        }
        //if there are not actions- only direct action available
            else{
                frappe.msgprint("No rows in actions")
                add_redirect_action(frm);           
            }
         
        }

    },

    category: function(frm) {

      // Clear previously added attach image fields
      frm.clear_table("attachments");

      // Fetch Transaction Type Requirements based on the selected Transaction Type
      if (frm.doc.category) {
        frappe.call({
          method: "academia.transaction_management.doctype.transaction.transaction.get_transaction_category_requirement",
          args: {
            transaction_category: frm.doc.category
          },
          callback: function(response) {
            // Add attach image fields for each Transaction Type Requirement
            const requirements = response.message || [];

            requirements.forEach(function(requirement) {
              const fieldname =  requirement.name.replace(/ /g, "_").toLowerCase()+"_file";

              frm.add_child("attachments", {
                attachment_name: fieldname,
                attachment_label: requirement.name,
                fieldtype: "Attach Image"
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
        frappe.prompt([
            {
                fieldname: 'party',
                label: __('Party'),
                fieldtype: 'Link',
                options: 'DocType',
                reqd: 1,
                get_query: function() {
                    return {
                        filters: [
                            ['DocType', 'name', 'in', ['Department', 'External Party']]
                        ]
                    };
                }
            },
            {
                fieldname: 'company',
                label: __('Company'),
                fieldtype: 'Link',
                options: 'Company',
                reqd: 1,
            },
            {
                fieldname: 'to_department',
                label: __('To Department'),
                fieldtype: 'Dynamic Link',
                options: 'party',
                reqd: 1
            },
            {
                fieldname: 'redirected_to',
                label: __('Redirect To'),
                fieldtype: 'Link',
                options: 'User',
                reqd: 1,
            },
            {
                fieldname: 'details',
                label: __('Details'),
                fieldtype: 'Text',
                reqd: 1,
            }
        ], function(values) {
            var childTable = cur_frm.add_child('actions');

            childTable.party = values.party;
            childTable.to_department = values.to_department;
            childTable.action_date = frappe.datetime.now_datetime();
            childTable.created_by = frappe.session.user;
            childTable.type = "Redirected";
            childTable.details = values.details;

            frappe.model.with_doc('User', values.redirected_to, function() {
                var user = frappe.model.get_doc('User', values.redirected_to);
                if (user) {
                    frappe.msgprint("there is user");
                    frappe.msgprint(user.name);
                    childTable.redirected_to = user.name;

                    // frappe.call({
                    //     method: "academia.transaction_management.doctype.transaction_action.transaction_action.create_user_permission",
                                                    
                    //     args: {
                    //         user: user.name, 
                    //         for_value: frm.doc.name
                    //     },
                    //     callback: function(response) {
                    //         if (response && response.message) {
                    //             console.log("Ok");
                    //         }
                    //     }
                    // });
                    
                    frappe.call({
                        method: "frappe.client.save",
                        args: {
                            doc: frm.doc
                        },
                        callback: function(response) {
                            if (response && response.message) {
                                location.reload();
                            }
                            frappe.msgprint(response.message);
                        }
                    });
                }
            });
        }, __('Redirect Transaction'));
    });
}


function add_recieve_action(frm) {
    cur_frm.page.add_action_item(__('Received'), function() {
        frappe.msgprint("Received")
       
        var childTable = cur_frm.add_child('actions');
       // childTable.party = values.party;
       // childTable.to_department = values.to_department;
        childTable.action_date = frappe.datetime.now_datetime();
        frappe.msgprint("field are filled")     
        childTable.created_by = frappe.session.user;
        childTable.type = "Received";
        frappe.msgprint("field are filled")
        frappe.call({
            method: "frappe.client.save",
            args: {
                doc: frm.doc
            },
            callback: function(response) {
                if (response && response.message) {
                    frappe.db.set_value('Transaction', frm.docname, 'status', 'Pending');
                    location.reload();
                }
                frappe.msgprint(response.message);
            }
        });
    });
}

function add_approve_action(frm) {
    cur_frm.page.add_action_item(__('Approve'), function() {
        // frappe.msgprint("Approve");

        frappe.prompt([
            {
                label: 'Details',
                fieldname: 'details',
                fieldtype: 'Text',
                reqd: 1
            }
        ], function(values) {
            var childTable = cur_frm.add_child('actions');
            childTable.action_date = frappe.datetime.now_datetime();
            childTable.created_by = frappe.session.user;
            childTable.type = "Approved";
            childTable.details = values.details;

            frappe.call({
                method: "frappe.client.save",
                args: {
                    doc: frm.doc
                },
                callback: function(response) {
                    if (response && response.message) {
                        frappe.db.set_value('Transaction', frm.docname, 'status', 'Approved');
                        location.reload();
                    }
                    frappe.msgprint(response.message);
                }
            });
        }, __('Enter Approval Details'), __('Submit'));
    });
}

function add_reject_action(frm) {
    cur_frm.page.add_action_item(__('Reject'), function() {
        // frappe.msgprint("Reject");

        frappe.prompt([
            {
                label: 'Details',
                fieldname: 'details',
                fieldtype: 'Text',
                reqd: 1
            }
        ], function(values) {
            var childTable = cur_frm.add_child('actions');
            childTable.action_date = frappe.datetime.now_datetime();
            childTable.created_by = frappe.session.user;
            childTable.type = "Rejected";
            childTable.details = values.details;

            frappe.call({
                method: "frappe.client.save",
                args: {
                    doc: frm.doc
                },
                callback: function(response) {
                    if (response && response.message) {
                        frappe.db.set_value('Transaction', frm.docname, 'status', 'Rejected');
                        location.reload();
                    }
                    frappe.msgprint(response.message);
                }
            });
        }, __('Enter Rejection Details'), __('Submit'));
    });
}


frappe.ui.form.on("Transaction", {
    onload: function(frm) {
        frm.set_query("name", function() {
            return {
                query: "academia.transaction_management.doctype.transaction.transaction.get_permission_query",
                filters: {
                    "doctype": "Transaction",
                    "for_list_view": false
                }
            };
        });
    }
});





