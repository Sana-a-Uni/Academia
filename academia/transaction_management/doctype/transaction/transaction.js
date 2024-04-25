// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Transaction", {
// 	refresh(frm) {

// 	},
// });


// restrect choosing of Incoming and Outgoing check box
frappe.ui.form.on('Transaction', {
    // refresh: function(frm) {
    //     frm.toggle_reqd('incoming', !frm.doc.outgoing);
    // },
    // outgoing: function(frm) {
    //     frm.doc.incoming = !frm.doc.outgoing;
    //     frm.refresh_field('incoming');
    // },
    // incoming: function(frm) {
    //     frm.doc.outgoing = !frm.doc.incoming;
    //     frm.refresh_field('outgoing');
    // }

    outgoing: function(frm) {
        if(frm.doc.outgoing){
            frm.doc.incoming = false;
        }
        frm.refresh_field('incoming');
    },
    incoming: function(frm) {
        if(frm.doc.incoming){
            frm.doc.outgoing = false;
        }
        frm.refresh_field('outgoing');
    }
});

// set the "Start Date" field to the current date by default 
frappe.ui.form.on('Transaction', {
    onload: function(frm) {
        if (!frm.doc.start_date) {
            frm.set_value('start_date', frappe.datetime.get_today());
        }
    }
});

///////////////////

// hide (From Department) and (To Department) until select (Incoming) or (Outgoing)

frappe.ui.form.on('Transaction', {
    incoming: function(frm) {
        toggleDepartmentFieldsVisibility(frm);
    },
    outgoing: function(frm) {
        toggleDepartmentFieldsVisibility(frm);
    },
    refresh: function(frm) {
        toggleDepartmentFieldsVisibility(frm);
    }
});

function toggleDepartmentFieldsVisibility(frm) {
    // Get references to the fields
    var fromDeptField = frm.fields_dict.from_department;
    var toDeptField = frm.fields_dict.to_department;
    
    var fromPartyField = frm.fields_dict.from_party;
    var toPartyField = frm.fields_dict.to_party;
    
    var subDepartment = frm.fields_dict.sub_department;

    // Check if either checkbox is checked
    var incomingChecked = frm.doc.incoming;
    var outgoingChecked = frm.doc.outgoing;

    // Set field visibility based on checkbox state
    fromDeptField.df.hidden = !incomingChecked;
    fromPartyField.df.hidden = !incomingChecked;
    
    toDeptField.df.hidden = !outgoingChecked;
    toPartyField.df.hidden = !outgoingChecked;

    subDepartment.df.hidden = incomingChecked && outgoingChecked;
    
    // Refresh the form to apply the visibility changes
    frm.refresh_field('from_department');
    frm.refresh_field('from_party');
    frm.refresh_field('to_department');
    frm.refresh_field('to_party');
    frm.refresh_field('sub_department');
}

////////////////////////////


frappe.ui.form.on('Transaction', {
    refresh: function(frm) {
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
        
    }
    
});

// frappe.ui.form.on('MyDocType', {
//     refresh: function(frm) {
//         // Set a query filter for the "party" field
//         frm.fields_dict.party.get_query = function(doc, cdt, cdn) {
//             return {
//                 filters: [
//                     ['DocType', 'name', 'in', ['Department', 'External Party']],
//                     ['DocType', 'name', 'not in', ['Department', 'External Party']]
//                 ],
//                 query: 'frappe.desk.search.search_link'
//             };
//         };

        // // Rename the options displayed in the "party" field
        // frm.fields_dict.party.get_query_options = function() {
        //     return {
        //         query: 'frappe.desk.search.search_link',
        //         filters: {
        //             'Department': 'Internal',
        //             'External Party': 'External'
        //         }
        //     };
//         // };
//     }
// });


// frappe.ui.form.on('Transaction', {
//     refresh: function(frm) {
//         // Check if the 'from_department' field has a value
//         if (frm.doc.from_department) {
//             frm.set_df_property('from_department', 'hidden', 0);
//         } else {
//             frm.set_df_property('from_department', 'hidden', 1);
//         }

//         if (frm.doc.to_department) {
//             frm.set_df_property('to_department', 'hidden', 0);
//         } else {
//             frm.set_df_property('to_department', 'hidden', 1);
//         }

        // if (frm.doc.from_party) {
        //     frm.set_df_property('from_party', 'hidden', 0);
        // } else {
        //     frm.set_df_property('from_party', 'hidden', 1);
        // }

        // if (frm.doc.to_party) {
        //     frm.set_df_property('to_party', 'hidden', 0);
        // } else {
        //     frm.set_df_property('to_party', 'hidden', 1);
        // }
//     }
// });


frappe.ui.form.on('Transaction', {
    incoming:function (frm) {
        if(frm.doc.from_department)
        {
            frm.set_value('sub_department_link', frm.doc.from_party);
            frm.set_value('sub_department', '');

        }
        else
        {
            frm.set_value('sub_department_link', '');
            frm.set_value('sub_department', '');
        }
        // Apply a filter on the sub_department field
        if(frm.doc.from_party == "Department")
        frm.set_query('sub_department', function() {
            return {
                filters: {
                    parent_department: frm.doc.from_department
                }
            };
        });
        if(frm.doc.from_party == "External Party")
        frm.set_query('sub_department', function() {
            return {
                filters: {
                    parent_external_party: frm.doc.from_department
                }
            };
        });
    },
    outgoing:function (frm) {
        if(frm.doc.to_department)
        {
            frm.set_value('sub_department_link', frm.doc.to_party);
            frm.set_value('sub_department', '');
        }
        else
        {
            frm.set_value('sub_department_link', '');
            frm.set_value('sub_department', '');
        }

        // Apply a filter on the sub_department field
        if(frm.doc.to_party == "Department")
        frm.set_query('sub_department', function() {
            return {
                filters: {
                    parent_department: frm.doc.to_department
                }
            };
        });
        if(frm.doc.to_party == "External Party")
        frm.set_query('sub_department', function() {
            return {
                filters: {
                    parent_external_party: frm.doc.to_department
                }
            };
        });
    },
    to_department: function(frm) {
        if (frm.doc.outgoing) {
            frm.set_value('sub_department_link', frm.doc.to_party);

            // Apply a filter on the sub_department field
            if(frm.doc.to_party == "Department")
            frm.set_query('sub_department', function() {
                return {
                    filters: {
                        parent_department: frm.doc.to_department
                    }
                };
            });
            if(frm.doc.to_party == "External Party")
            frm.set_query('sub_department', function() {
                return {
                    filters: {
                        parent_external_party: frm.doc.to_department
                    }
                };
            });
        }
    },
    from_department: function(frm) {
        if (frm.doc.incoming) {
            frm.set_value('sub_department_link', frm.doc.from_party);

            // Apply a filter on the sub_department field
            if(frm.doc.from_party == "Department")
            frm.set_query('sub_department', function() {
                return {
                    filters: {
                        parent_department: frm.doc.from_department
                    }
                };
            });
            if(frm.doc.from_party == "External Party")
            frm.set_query('sub_department', function() {
                return {
                    filters: {
                        parent_external_party: frm.doc.from_department
                    }
                };
            });
        }
    }
});
// frappe.ui.form.on('Transaction', {
//     from_department: function(frm) {
//         if (frm.doc.outgoing) {
//             frm.set_value('sub_department_link', frm.doc.to_party);

//             // Apply a filter on the sub_department field
//             frm.set_query('sub_department', function() {
//                 return {
//                     filters: {
//                         parent_department: frm.doc.from_department
//                     }
//                 };
//             });
//         }
//     }
// });
