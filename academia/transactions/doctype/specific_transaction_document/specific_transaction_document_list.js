frappe.listview_settings['Specific Transaction Document'] = {
    onload: function(listview) {
        $('.btn-primary').filter(function () {
            return $(this).text().trim() === 'Add Specific Transaction Document';
        }).hide();

        if(!frappe.user_roles.includes('Transactions Manager')) {
            frappe.call({
                method: 'academia.transactions.doctype.specific_transaction_document.specific_transaction_document.get_shared_std',
                args: {
                    user: frappe.session.user
                },
                callback: function(response) {
                    if (response.message) {
                        const allowed_std = response.message;
                        listview.filter_area.add([
                            ['Specific Transaction Document', 'name', 'in', allowed_std]
                        ]);
    
                        $('.filter-selector').hide();
                    }
                }
            });
        }
    }
};