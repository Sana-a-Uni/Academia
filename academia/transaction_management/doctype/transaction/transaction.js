// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt


frappe.ui.form.on('Transaction', {
    
    onload: function(frm) {
        if (!frm.doc.start_date) {
            frm.set_value('start_date', frappe.datetime.get_datetime_as_string());
        }

        // frappe.call({
        //     method: "academia.transaction_management.doctype.transaction.transaction.render_vertical_path",

        //     args: {
        //         transaction: frm.doc.name,
        //     },
        //     callback: function(response) {
        //         if (response.message) {
        //             // Handle the response as required
        //             console.log(response.message);
        //         }
        //     }
        // });

    },
    refresh: function(frm) {

        if(frm.doc.docstatus === 1 && !frm.doc.__islocal )
        {
            frappe.call({
                method: 'academia.transaction_management.doctype.transaction.transaction.get_last_transaction_action_status',
                args: { 
                    transaction: frm.doc.name,
                },
                callback: function(response) {
                    if (response.message) {
                        if(response.message == "Approved")
                            frappe.db.set_value('Transaction', frm.docname, 'status', 'Approved');

                        else if(response.message == "Rejected")
                            frappe.db.set_value('Transaction', frm.docname, 'status', 'Rejected');
    
                        else if(response.message == "Redirected")
                        {
                            frappe.db.set_value('Transaction', frm.docname, 'status', 'Pending');
                            cur_frm.page.add_action_item(__('Received'), function() {
                                frappe.call({
                                    method: 'academia.transaction_management.doctype.transaction_action.transaction_action.receive_transaction',
                                    args: { 
                                        main_transaction: frm.doc.name,
                                    },
                                    callback: function(response) {
                                        if (response.message) {
                                            frappe.msgprint(__(response.message));
                                            cur_frm.reload_doc();

                                            frm.page.actions.find('[data-label="Received"]').parent().parent().remove();
                                        }
                                    }       
                                });
                            });
                        }
    
                        else if(response.message == "Received")
                        {
                            cur_frm.page.add_action_item(__('Approve'), function() {
                                frappe.call({
                                    method: 'academia.transaction_management.doctype.transaction_action.transaction_action.approve_transaction',
                                    args: { 
                                        main_transaction: frm.doc.name,
                                    },
                                    callback: function(response) {
                                        if (response.message) {
                                            frappe.msgprint(__(response.message));
                                            frm.$wrapper.Find('.actions-btn-group .dropdown-menu ').parent().addClass('hidden');
                                            frm.page.actions.find('[data-label="Approve"]').parent().parent().remove();
                                            frm.page.actions.find('[data-label="Redirect"]').parent().parent().remove();
                                            frm.page.actions.find('[data-label="Reject"]').parent().parent().remove();

                                            cur_frm.reload_doc();

                                        }
                                    }       
                                });
                            });
                
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
                                        fieldname: 'to_department',
                                        label: __('To Department'),
                                        fieldtype: 'Dynamic Link',
                                        options: 'party',
                                        reqd: 1
                                    },
                                    {
                                        fieldname: 'redirect_to',
                                        label: __('Redirect To'),
                                        fieldtype: 'Link',
                                        options: 'User',
                                        reqd: 1,
                                    }
                                ]
                                , function(values){
                
                                    var party = values.party;
                                    var to_department = values.to_department;
                                    var redirect_to = values.redirect_to;
                                    frappe.call({
                                        method: 'academia.transaction_management.doctype.transaction_action.transaction_action.redirect_transaction',
                                        args: {
                                            main_transaction : frm.doc.name,
                                            party: party,
                                            to_department: to_department,
                                            redirect_to: redirect_to,
                                        },
                                        callback: function(response) {
                                            if (response.message) {
                                                frappe.msgprint(__(response.message));
                                                frm.$wrapper.Find('.actions-btn-group .dropdown-menu ').parent().addClass('hidden');
                                                frm.page.actions.find('[data-label="Approve"]').parent().parent().remove();
                                                frm.page.actions.find('[data-label="Redirect"]').parent().parent().remove();
                                                frm.page.actions.find('[data-label="Reject"]').parent().parent().remove();

                                                cur_frm.reload_doc();

                                            }
                                        }
                                    });
                                    }, __('Redirect Transaction'));
                            });
                
                            cur_frm.page.add_action_item(__('Reject'), function() {
                                frappe.call({
                                    method: 'academia.transaction_management.doctype.transaction_action.transaction_action.reject_transaction',
                                    args: { 
                                        main_transaction: frm.doc.name,
                                    },
                                    callback: function(response) {
                                        if (response.message) {
                                            frappe.msgprint(__(response.message));
                                            
                                            frm.$wrapper.Find('.actions-btn-group .dropdown-menu ').parent().addClass('hidden');
                                            frm.page.actions.find('[data-label="Approve"]').parent().parent().remove();
                                            frm.page.actions.find('[data-label="Redirect"]').parent().parent().remove();
                                            frm.page.actions.find('[data-label="Reject"]').parent().parent().remove();

                                            cur_frm.reload_doc();
                                        }
                                    }
                                });
                            });
                        }
                        
                        else if(response.message == "Canceld")
                            frappe.db.set_value('Transaction', frm.docname, 'status', 'Canceld');
                    }
    
                    // if there isnt any transaction action
                    else
                    {
    
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
                                    fieldname: 'to_department',
                                    label: __('To Department'),
                                    fieldtype: 'Dynamic Link',
                                    options: 'party',
                                    reqd: 1
                                },
                                {
                                    fieldname: 'redirect_to',
                                    label: __('Redirect To'),
                                    fieldtype: 'Link',
                                    options: 'User',
                                    reqd: 1,
                                }
                            ]
                            , function(values){
            
                                var party = values.party;
                                var to_department = values.to_department;
                                var redirect_to = values.redirect_to;
                                frappe.call({
                                    method: 'academia.transaction_management.doctype.transaction_action.transaction_action.redirect_transaction',
                                    args: {
                                        main_transaction : frm.doc.name,
                                        party: party,
                                        to_department: to_department,
                                        redirect_to: redirect_to,
                                    },
                                    callback: function(response) {
                                        if (response.message) {
                                            frappe.msgprint(__(response.message));

                                            frm.page.actions.find('[data-label="Approve"]').parent().parent().remove();
                                            frm.page.actions.find('[data-label="Redirect"]').parent().parent().remove();
                                            frm.page.actions.find('[data-label="Reject"]').parent().parent().remove();
                                            
                                            cur_frm.reload_doc();

                                        }
                                    }
                                });
                                }, __('Redirect Transaction'));
                        });
                    }
                }
            });
        }

        // to display the Transaction Action
        frm.trigger('showTransactionActions');

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


    showTransactionActions: async function(frm) {
        await frappe.call({
          method: 'academia.transaction_management.doctype.transaction.transaction.get_transaction_actions',
          args: { transaction: frm.doc.name },
          callback: function(response) {
              if (response.message !== null && response.message.length > 0) {
                
                frm.set_df_property("summary_section", "hidden", 0);
                frm.refresh_field("summary_section");

                  // Display the association transactions
                  var TransactionActions = response.message;
  
                  let html = `
                  <div class="form-grid-container">
                      <div class="form-grid">
                          <div class="grid-heading-row">
                              <div class="grid-row">
                                  <div class="data-row row">
                                      <div class="row-index sortable-handle col col-xs-1">
                                          <span>No.</span>
                                      </div>`;
                  const columnNames = Object.keys(TransactionActions[0]);
                  
              columnNames.filter(column => column === "name" || column === "type").forEach(column => {
              html += `
                                      <div class="col grid-static-col col-xs-2">
                                          ${column}
                                      </div>`
                                  });

                      html += `
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
                  <div class="grid-body">
                      <div class="rows">
                          <div class="grid-row"">
                  `;
  
                  // Loop over TransactionActions array
                  TransactionActions.forEach((transaction, index) => {
                      var link = frappe.utils.get_form_link("Transaction Action", transaction.name)

                      html += `                    
                          <a href="${link}"> 
                              <div class="data-row row m-2">
                                  <div class="col grid-static-col col-xs-1 bold">
                                          ${index + 1 }
                                  </div>
                                  <div class="col grid-static-col col-xs-2 bold">
                                          ${transaction.name}
                                  </div>
                                  <div class="col grid-static-col col-xs-2 bold">
                                          ${transaction.type}
                                  </div>
                              </div>
                          </a>
                          <hr>
                      `;
                  });
  
                  html += `
                          </div>
                      </div>
                  </div>`;
                  frm.set_df_property("summary", "options", html);
                  frm.refresh_field("summary");

              }else{

                frm.set_df_property("summary_section", "hidden", 1);
                frm.refresh_field("summary_section");
              }
          }
      });
  },
});
