// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Council Memo", {
  refresh(frm) {
    // Add a custom button to assign the topic to a council
    if (frm.doc.docstatus === 1) {
      frm.add_custom_button(__("Create Assignment from Memo"), function () {
        frappe.db.count('Topic Assignment',  { filters: { initiating_council_memo: ['=',frm.doc.name] }})
        .then(count => {
          if (count === 0) {
            frappe.db.get_doc('Topic Assignment', frm.doc.originating_assignment)
          .then(doc => {
            // console.log(`${!doc.is_group}`);
            frappe.new_doc("Topic Assignment",{
              council:frm.doc.council,
              topic: doc.topic,
              main_category: doc.main_category,
              sub_category: doc.sub_category,
              initiating_council_memo: frm.doc.name,
            });    
          });
          }else{
            frm.remove_custom_button(__("Create Assignment from Memo"));
            frappe.throw(__("This Council Memo already has an Assignment"));
          }
        });
      });


    }
  },
});
