// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt


frappe.ui.form.on('Transaction', {
    
    outgoing: function(frm) {
        if (frm.doc.outgoing) {
            frm.doc.incoming = false;
            setSubDepartmentQuery(frm, frm.doc.to_party, frm.doc.to_department);
        }
        toggleDepartmentFieldsVisibility(frm);
        frm.refresh_field('incoming');
    },
    incoming: function(frm) {
        if (frm.doc.incoming) {
            frm.doc.outgoing = false;
            setSubDepartmentQuery(frm, frm.doc.from_party, frm.doc.from_department);
        }
        toggleDepartmentFieldsVisibility(frm);
        frm.refresh_field('outgoing');
    },
    onload: function(frm) {
        if (!frm.doc.start_date) {
            frm.set_value('start_date', frappe.datetime.get_today());
        }
    },
    refresh: function(frm) {

        frm.trigger('showAssociatedTransactions');

        
        toggleDepartmentFieldsVisibility(frm);
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
    },
    to_department: function(frm) {
        if (frm.doc.outgoing) {
            frm.set_value('sub_department_link', frm.doc.to_party);
            setSubDepartmentQuery(frm, frm.doc.to_party, frm.doc.to_department);
        }
    },
    from_department: function(frm) {
        if (frm.doc.incoming) {
            frm.set_value('sub_department_link', frm.doc.from_party);
            setSubDepartmentQuery(frm, frm.doc.from_party, frm.doc.from_department);
        }
    },
    //
    showAssociatedTransactions: async function(frm) {
        if (frm.doc.associated_transaction) {
          await frm.trigger("displayTransactionArray");
            frm.refresh_field("associated_transactions");
            frm.set_df_property("associated_transactions_section", "hidden", 0);
          
        }
        else {
            frm.set_df_property("associated_transactions_section", "hidden", 1);
        }
    },
    async displayTransactionArray(frm) {
        await frappe.call({
            method: 'academia.transaction_management.doctype.transaction.transaction.get_associated_transactions',
            args: { associated_transaction: frm.doc.associated_transaction },
            callback: function(response) {
                if (response.message) {
                    // Display the association transactions
                    var associationTransactions = response.message;
    
                    let html = `
                    <div class="form-grid-container">
                        <div class="form-grid">
                            <div class="grid-heading-row">
                                <div class="grid-row">
                                    <div class="data-row row">
                                        <div class="row-index sortable-handle col col-xs-1">
                                            <span>No.</span>
                                        </div>`;
                    const columnNames = Object.keys(associationTransactions[0]);
                    
                columnNames.filter(column => column === "name" || column === "start_date" || column === "from_department" || column === "to_department").forEach(column => {
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
    
                    // Loop over associationTransactions array
                    associationTransactions.forEach((transaction, index) => {
                        var link = frappe.utils.get_form_link("Transaction", transaction.name)

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
                                    ${transaction.from_department}
                                            
                                    </div>
                                    <div class="col grid-static-col col-xs-2 bold">
                                            ${transaction.to_department}
                                    </div>
                                    <div class="col grid-static-col col-xs-2 bold">
                                            
                                            ${transaction.start_date}
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
    
                    frm.set_df_property("associated_transactions", "options", html);
                }
            }
        });
    },
    category: function(frm) {
        console.log("eeee")
        // Clear previously added attach image fields
        frm.clear_table("attachments");

        // Fetch Transaction Type Requirements based on the selected Transaction Type
        if (frm.doc.category) {
          frappe.call({
            method: "academia.transaction_management.server_scripts.get_transaction_category_requirement",
            args: {
              transaction_category: frm.doc.category
            },
            callback: function(response) {
              // Add attach image fields for each Transaction Type Requirement
              const requirements = response.message || [];
              //console.log("REQUIRMTS"+requirements)
              requirements.forEach(function(requirement) {
                const fieldname =  requirement.name.replace(/ /g, "_").toLowerCase()+"_file";
                //console.log("field name: "+fieldname)

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

            //   // Save the form to reflect the changes
            //   frm.save();
            }
          });
        }

        // Show a message when the Type field is changed
        //frappe.msgprint("Type field changed!");
      },
});


function toggleDepartmentFieldsVisibility(frm) {
    var fromDeptField = frm.fields_dict.from_department;
    var toDeptField = frm.fields_dict.to_department;
    var fromPartyField = frm.fields_dict.from_party;
    var toPartyField = frm.fields_dict.to_party;
    var subDepartment = frm.fields_dict.sub_department;

    var incomingChecked = frm.doc.incoming;
    var outgoingChecked = frm.doc.outgoing;

    fromDeptField.df.hidden = !incomingChecked;
    fromPartyField.df.hidden = !incomingChecked;
    toDeptField.df.hidden = !outgoingChecked;
    toPartyField.df.hidden = !outgoingChecked;
    subDepartment.df.hidden = !(incomingChecked || outgoingChecked);


    frm.refresh_field('from_department');
    frm.refresh_field('from_party');
    frm.refresh_field('to_department');
    frm.refresh_field('to_party');
    frm.refresh_field('sub_department');
}

function setSubDepartmentQuery(frm, party, department) {
    if (party) {
        frm.set_value('sub_department_link', party);
        frm.set_value('sub_department', '');

        var filter = {};
        if (party === 'Department') {
            filter.parent_department = department;
        } else if (party === 'External Party') {
            filter.parent_external_party = department;
        }

        frm.set_query('sub_department', function() {
            return {
                filters: filter
            };
        });
    } else {
        frm.set_value('sub_department_link', '');
        frm.set_value('sub_department', '');
    }
    
}