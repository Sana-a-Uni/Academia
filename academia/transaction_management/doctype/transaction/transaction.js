// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt


frappe.ui.form.on('Transaction', {
    
    onload: function(frm) {
        if (!frm.doc.start_date) {
            frm.set_value('start_date', frappe.datetime.get_today());
        }
    },
    refresh: function(frm) {
        // display the custom button after save the document
        if (!frm.doc.__islocal)
        {
            frm.add_custom_button('Transaction Action', function() {
                frappe.new_doc('Transaction Action', {
                    'main_transaction': frm.doc.name
                });
            }).addClass('btn-primary');    
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
                  
              columnNames.filter(column => column === "name" ).forEach(column => {
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
