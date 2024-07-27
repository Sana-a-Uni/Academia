
function go_to_transaction(refrenced_transaction) {
  
       if (refrenced_transaction){

           frappe.set_route('Form', 'Transaction', refrenced_transaction);
          
   }
}


frappe.ui.form.on('Test Transaction For Other Modules', {

    test_create_transaction: function(frm) {
        //applicant_type: "Student","Employee","User","Academic"
         applicants = [
            { applicant_type: "Student", applicant: "EDU-STU-2024-00001", applicant_name: "Hala" },
            { applicant_type: "Employee", applicant: "HR-EMP-00002", applicant_name: "Mansour" }
        ];

       
        applicants = JSON.stringify(applicants);

        frappe.call({
            method: "academia.transaction_management.doctype.transaction.transaction.create_transaction",
            args: {
                priority: "Low",
                title: "Transaction Title",   
                category: "Main Cat",
                sub_category: "Sub Cat",
                refrenced_document: "HR-EMP-00002",
                applicants_list: applicants,
              

            },
            callback: function(r) {
                console.log(r); // Log the response object to the console for debugging
    
                // Check if the response contains the 'message' property
                if (r && r.message) {
                    // Access the transaction ID from the response
                    const transactionId = r.message;
                    // frappe.msgprint("Transaction ID: " + transactionId);
    
                    frm.set_value("referenced_transaction", transactionId);
                    go_to_transaction(transactionId,applicants,frm)

                 
    
                    
                } else {
                    console.error("Unexpected response format");
                }
            }
        });

    
       
    }
});



