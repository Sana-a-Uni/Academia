frappe.listview_settings['Request'] = {
    onload: function(listview) {
        $('.btn-primary').filter(function () {
            return $(this).text().trim() === 'Add Request';
        }).hide();

        if(!frappe.user_roles.includes('Transactions Manager')) {
            frappe.call({
                method: 'academia.transactions.doctype.request.request.get_shared_requests',
                args: {
                    user: frappe.session.user
                },
                callback: function(response) {
                    if (response.message) {
                        const allowed_memos = response.message;
                        listview.filter_area.add([
                            ['Request', 'name', 'in', allowed_memos]
                        ]);
    
                        $('.filter-selector').hide();
                    }
                }
            });
        }
    }
};