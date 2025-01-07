frappe.listview_settings['Inbox Memo'] = {
    onload: function() {
        $('.btn-primary').filter(function () {
            return $(this).text().trim() === 'Add Inbox Memo';
        }).hide();
    }
};
// frappe.listview_settings['Inbox Memo'] = {
//     onload: function(listview) {
//         // Fetch the current user's employee name
//         frappe.call({
//             method: 'frappe.client.get_value',
//             args: {
//                 doctype: 'Employee',
//                 filters: { 'user_id': frappe.session.user },
//                 fieldname: 'name'
//             },
//             callback: function(response) {
//                 if (response.message) {
//                     const employee_name = response.message.name;

//                     // Add a filter to show only records where the recipients child table contains the employee name
//                     listview.page.add_inner_button(__('Show My Memos'), function() {
//                         listview.filter_area.add([
//                             ['Inbox Memo', 'Recipient (Transaction Recipients New)', 'like', '%' + employee_name + '%']
//                         ]);
//                     });

//                     // Apply the filter automatically on load
//                     listview.filter_area.add([
//                         ['Inbox Memo', 'Recipient (Transaction Recipients New)' , 'like', '%' + employee_name + '%']
//                     ]);
//                 }
//             }
//         });
//     }
// };