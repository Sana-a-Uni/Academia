frappe.listview_settings['Transaction New'] = {

    onload: function(listview) {
        // $('.btn-primary').filter(function () {
        //     return $(this).text().trim() === 'Add Inbox Memo';
        // }).hide();

        if(!frappe.user_roles.includes('Transactions Manager')) {
            frappe.call({
                method: 'academia.transactions.doctype.transaction_new.transaction_new.get_shared_transactions',
                args: {
                    user: frappe.session.user
                },
                callback: function(response) {
                    if (response.message) {
                        const allowed_transactions = response.message;
                        listview.filter_area.add([
                            ['Transaction New', 'name', 'in', allowed_transactions]
                        ]);
    
                        $('.filter-selector').hide();
                    }
                }
            });
        }
    }
};