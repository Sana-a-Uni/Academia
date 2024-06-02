// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction Action", {
	refresh: function(frm) {

//         // show Approve, Redirect and Reject actions if the document is draft and saved
//         if(frm.doc.docstatus === 0 && !frm.doc.__islocal ){
            
//             // after amend from another Transaction Action change the status to be Open
//             if(frm.doc.status === "Approved")
//             {
//                 frm.set_value('status', "Open");
//                 frm.save();
//             }
//             else if(frm.doc.status === "Open")
//             {
//                 frm.page.clear_primary_action();

//                 // change it to pyothn script if you need
//                 cur_frm.page.add_action_item(__('Received'), function() {
//                     frm.set_value('status', "Received");
//                     frm.set_value('receive_date', frappe.datetime.get_datetime_as_string());
//                     frm.save();
//                 });
//             }
//             else if(frm.doc.status === "Received")
//             {

//                 // clear all actions and add only what we need 
//                 frm.page.clear_actions();

//                 // add Approve to actions
//                 cur_frm.page.add_action_item(__('Approve'), function() {
//                     frappe.call({
//                         method: 'academia.transaction_management.doctype.transaction_action.transaction_action.approve_transaction',
//                         args: { 
//                             doctype: "Transaction Action",
//                             docname: frm.doc.name,
//                         },
//                         callback: function(response) {
//                             if (response.message) {
//                                 frappe.msgprint(__(response.message));
//                                 deleteActionItems(frm, 'Approve', 'Redirect', 'Reject')
//                             }
                             
//                         }
//                     });
//                 });

//                 cur_frm.page.add_action_item(__('Redirect'), function() {
//                     frappe.prompt([
//                         {
//                             fieldname: 'party',
//                             label: __('Party'),
//                             fieldtype: 'Link',
//                             options: 'DocType',
//                             reqd: 1,
//                             get_query: function() {
//                                 return {
//                                     filters: [
//                                         ['DocType', 'name', 'in', ['Department', 'External Entity']]
//                                     ]
//                                 };
//                             }
//                         },
//                         {
//                             fieldname: 'to_department',
//                             label: __('To Department'),
//                             fieldtype: 'Dynamic Link',
//                             options: 'party',
//                             reqd: 1
//                         },
//                         {
//                             fieldname: 'redirect_to',
//                             label: __('Redirect To'),
//                             fieldtype: 'Link',
//                             options: 'User',
//                             reqd: 1,
//                         }
//                     ]
//                     , function(values){
    
//                         var party = values.party;
//                         var to_department = values.to_department;
//                         var redirect_to = values.redirect_to;

//                         frappe.call({
//                             method: 'academia.transaction_management.doctype.transaction_action.transaction_action.redirect_transaction',
//                             args: { 
//                                 doctype: "Transaction Action",
//                                 docname: frm.doc.name, 
//                                 party: party,
//                                 to_department: to_department,
//                                 redirect_to: redirect_to,
//                             },
//                             callback: function(response) {
//                                 if (response.message) {
//                                     frappe.msgprint(__(response.message));

//                                     deleteActionItems(frm, 'Approve', 'Redirect', 'Reject')
//                                 }
                                 
//                             }
//                         });
//                         }, __('Redirect Transaction'));
//                 });

//                 cur_frm.page.add_action_item(__('Reject'), function() {
//                     frappe.call({
//                         method: 'academia.transaction_management.doctype.transaction_action.transaction_action.reject_transaction',
//                         args: { 
//                             doctype: "Transaction Action",
//                             docname: frm.doc.name,
//                         },
//                         callback: function(response) {
//                             if (response.message) {
//                                 frappe.msgprint(__(response.message));

//                                 deleteActionItems(frm, 'Approve', 'Redirect', 'Reject')
//                             }
//                         }
//                     });
//                 });
//             }
//         }
//         else if(frm.doc.docstatus === 1){
            
//             // to delete the default cancel button
//             cur_frm.page.btn_secondary.hide();

//             cur_frm.page.add_action_item(__('Cancel'), function() {

//                 frappe.call({
//                     method: 'academia.transaction_management.doctype.transaction_action.transaction_action.cancel_transaction_action',
//                     args: { 
//                         doctype: "Transaction Action",
//                         docname: frm.doc.name,
//                     },
//                     callback: function(response) {
//                         if (response.message) {
//                             frappe.msgprint(__(response.message));

//                             deleteActionItems(frm, 'Cancel')
//                         }
                         
//                     }
//                 });
//             });
//         }

//         if(frm.doc.main_transaction){
//             // to display main_transaction_information_section
//             frm.trigger('showMainTransactionInformation');
//         }
//         // filter party field
//         frm.fields_dict.party.get_query = function(doc, cdt, cdn) {
//             return {
//                 filters: [
//                     ['DocType', 'name', 'in', ['Department', 'External Entity']]
//                 ]
//             };
//         };

	},
//     showMainTransactionInformation: async function(frm) {
//         await frappe.call({
//             method: 'academia.transaction_management.doctype.transaction_action.transaction_action.get_main_transaction_information',
//             args: { 
//                 transaction: frm.doc.main_transaction
//             },
//             callback: function(response) {
//                 if (response.message) {

//                 frm.set_df_property("main_transaction_information_section", "hidden", 0);
//                 frm.refresh_field("main_transaction_information_section");

//                   // Display the association transactions
//                   var MainTransaction = response.message;
  
//                   let html = `<div>`;
  
//                   // Loop through all fields in MainTransaction
//                   for (var field in MainTransaction) {
//                       if (field !== null) {
//                           // Add only the fields that have a value
//                           html += `<div>${field}: ${MainTransaction[field]}</div><br>`;
//                       }
//                   }
    
//                   html += `</div>`;
  
//                   frm.set_df_property("main_transaction_information", "options", html);
//                   frm.refresh_field("main_transaction_information");

//               }else{

//                 frm.set_df_property("main_transaction_information_section", "hidden", 1);
//                 frm.refresh_field("main_transaction_information_section");
//               }
//           }
//       });
//   },

});

// function deleteActionItems(frm, ...labels) {
//     labels.forEach(label => {
//         frm.page.actions.find(`[data-label="${label}"]`).parent().parent().remove();
//         cur_frm.reload_doc();
//     });
// }