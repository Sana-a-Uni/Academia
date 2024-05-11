// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction Action", {
    outgoing: function(frm) {
        // only one checkbox can be cheched
        if (frm.doc.outgoing) {
            frm.doc.incoming = false;
        }
        toggleDepartmentFieldsVisibility(frm);
        frm.refresh_field('incoming');
    },
    incoming: function(frm) {
        if (frm.doc.incoming) {
            frm.doc.outgoing = false;
        }
        toggleDepartmentFieldsVisibility(frm);
        frm.refresh_field('outgoing');
    },
	refresh: function(frm) {
        toggleDepartmentFieldsVisibility(frm);

        if(frm.doc.main_transaction){
            // to display main_transaction_information_section
            frm.trigger('showMainTransactionInformation');
        }
        // filter party fields
        frm.fields_dict.from_party.get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['DocType', 'name', 'in', ['Department', 'External Party']]
                ]
            };
        };
        frm.fields_dict.to_party.get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['DocType', 'name', 'in', ['Department', 'External Party']]
                ]
            };
        };

        // add custom button into incoming Transaction
        if (frm.doc.islocal || !frm.doc.incoming) {
            // Hide the button for new unsaved transactions and non-incoming transactions
            cur_frm.toggle_enable(('Issue Outgoing'), false);
            
        } else {
            // Show the button for saved incoming transactions without an outgoing transaction
            frm.add_custom_button('Issue Outgoing', function() {
                // Create a new transaction
                frappe.new_doc('Transaction Action', {
                    outgoing: 1, // Check the Outgoing checkbox
                    main_transaction: frm.doc.main_transaction, // Set the Transaction Parent field with the ID of the incoming transaction
                    to_party: frm.doc.from_party, // Set the Party link field with the same value as in transaction1
                    to_department: frm.doc.from_department,

                }, function(doc) {
                    // Save the new transaction
                    doc.outgoing = 1; // Manually set the Outgoing field value to ensure the checkbox is checked
                    doc.insert().then(function() {
                        // Navigate to the newly created transaction
                        frappe.set_route('Form', 'Transaction Action', doc.name);
                    });
                });
            }).addClass('btn-primary'); // Add a CSS class to the button to set its color to black

        }
	},
    showMainTransactionInformation: async function(frm) {
        await frappe.call({
            method: 'academia.transaction_management.doctype.transaction_action.transaction_action.get_main_transaction_information',
            args: { transaction: frm.doc.main_transaction },
            callback: function(response) {
                if (response.message) {

                frm.set_df_property("main_transaction_information_section", "hidden", 0);
                frm.refresh_field("main_transaction_information_section");

                  // Display the association transactions
                  var MainTransaction = response.message;
  
                  let html = `<div>`;
  
                  // Loop through all fields in MainTransaction
                  for (var field in MainTransaction) {
                      if (field !== null) {
                          // Add only the fields that have a value
                          html += `<div>${field}: ${MainTransaction[field]}</div><br>`;
                      }
                  }
    
                  html += `</div>`;
  
                  frm.set_df_property("main_transaction_information", "options", html);
                  frm.refresh_field("main_transaction_information");

              }else{

                frm.set_df_property("main_transaction_information_section", "hidden", 1);
                frm.refresh_field("main_transaction_information_section");
              }
          }
      });
  },

});



function toggleDepartmentFieldsVisibility(frm) {
    var fromDeptField = frm.fields_dict.from_department;
    var toDeptField = frm.fields_dict.to_department;
    var fromPartyField = frm.fields_dict.from_party;
    var toPartyField = frm.fields_dict.to_party;

    var incomingChecked = frm.doc.incoming;
    var outgoingChecked = frm.doc.outgoing;

    fromDeptField.df.hidden = !incomingChecked;
    fromPartyField.df.hidden = !incomingChecked;
    toDeptField.df.hidden = !outgoingChecked;
    toPartyField.df.hidden = !outgoingChecked;


    frm.refresh_field('from_department');
    frm.refresh_field('from_party');
    frm.refresh_field('to_department');
    frm.refresh_field('to_party');
}