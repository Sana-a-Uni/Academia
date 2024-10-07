frappe.ui.form.on('Student Applicant', {
    program_degree: function(frm) {
           
    
    var program_degree = frm.doc.program_degree;
    var academic_program = frm.doc.academic_program;
    frm.set_query("academic_program", function() {
        return {
            "filters": {
                "program_degree": program_degree
            }
        };
    });
        if (frm.doc.program_degree) {
            frappe.call({
                method: 'academia.admission.doctype.student_applicant.student_applicant.select_data',
                args: {
                    condition_value: frm.doc.program_degree 
                },
                callback: function(r) {
                    
                        frm.clear_table("qualification");
                        r.message.forEach(function(row) {
                            var child = frm.add_child("qualification");
                            child.name1 = row.qualification_type; 
                            
                        });
                        frm.refresh_field("qualification");
                }
            });
            frappe.call({
                method: 'academia.admission.doctype.student_applicant.student_applicant.get_document',
                args: {
                    condition_value: program_degree
                },
                callback: function(r) {
                    
                           
                        frm.clear_table("document");

                        
                        r.message.forEach(function(row) {
                            var child = frm.add_child("document");
                            child.name1 = row.document_type; 
                            
                        });

                        
                        frm.refresh_field("document");

                    
                }
            });
            }
    },
        // Function to set the query for the MultiSelect field
    
    refresh: function(frm) {
      var academic_program = frm.doc.academic_program;
      frm.set_query("course_code","remedial_materials", function() {
          return {
              "filters": {
                  "program": academic_program
              }
          };
      });
        if(frm.doc.docstatus === 0){
           
          if(frm.doc.status=='Draft'){  
            frm.add_custom_button(__('Verification'), function() {   
              frappe.call({
                    method: 'academia.admission.doctype.student_applicant.student_applicant.update_statues',
                    args: {
                      condition_value: frm.doc.name,
                      status:"Verification"
                  },  
                });
                frappe.show_alert({
                  message: __('the statues was succsuful changed to Verification'),
                  indicator: 'green'
                });
                frm.reload_doc();
                setTimeout(function() {
                  frm.reload_doc();
              }, 1000);
            }, __('Status'));
          }  
          else if(frm.doc.status === "Verification"){
            frm.add_custom_button(__('Accepted '), function() {   
              frappe.call({
                method: 'academia.admission.doctype.student_applicant.student_applicant.update_statues',
                args: {
                      condition_value: frm.doc.name,
                      status:"Accepted"
                  },
                    
                });
                frappe.show_alert({
                  message: __('the statues was succsuful changed to Accepted'),
                  indicator: 'green'
                });
                frm.reload_doc();
                setTimeout(function() {
                  frm.reload_doc();
              }, 1000);
               
            }, __('Status'));
          }
          
          if(frm.doc.status === 'Verification' || frm.doc.status === 'Draft') {  
            frm.add_custom_button(__('Rejected'), function() {   
                let d = new frappe.ui.Dialog({
                    title: 'Reject Student Application',
                    fields: [
                        {
                            label: 'Rejection Reason',
                            fieldname: 'rejection_reason',
                            fieldtype: 'Small Text',
                            reqd: 1
                        },
                        {
                            label: 'Email Subject',
                            fieldname: 'email_subject',
                            fieldtype: 'Data',
                            default: 'Your Application Status',
                            reqd: 1
                        },
                        {
                            label: 'Email Message',
                            fieldname: 'email_message',
                            fieldtype: 'Text',
                            reqd: 1
                        }
                    ],
                    primary_action_label: 'Send Email',
                    primary_action(values) {
                        frappe.call({
                            method: 'academia.admission.doctype.student_applicant.student_applicant.reject_student_application',
                            args: {
                                docname: frm.doc.name,
                                rejection_reason: values.rejection_reason,
                                email_subject: values.email_subject,
                                email_message: values.email_message
                            },
                            callback: function(r) {
                                if (r.message) {
                                    frappe.show_alert({
                                        message: __('The status was successfully changed to Rejected and email sent'),
                                        indicator: 'red'
                                    });
                                    d.hide();
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                });
                d.show();
            }, __('Status'));
        }
          
    
        }
        
        },
       

        
   
});

frappe.listview_settings['Student Applicant'] = {
    add_fields: ['status'],
    get_indicator: function(doc) {
        // Customize how indicators appear in the list view
        if (doc.status === 'Accepted') {
            return [__('Accepted'), 'green', 'status,=,Accepted'];
        } else if (doc.status === 'Rejected') {
            return [__('Rejected'), 'red', 'status,=,Rejected'];
        } else if (doc.status === 'Verification') {
            return [__('Verification'), 'orange', 'status,=,Verification'];
        } 
    }
  };