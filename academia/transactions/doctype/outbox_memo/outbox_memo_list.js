frappe.listview_settings['Outbox Memo'] = {
    onload: function(listview) {
        $('.btn-primary').filter(function () {
            return $(this).text().trim() === 'Add Outbox Memo';
        }).hide();

        if(!frappe.user_roles.includes('Transactions Manager')) {
            frappe.call({
                method: 'academia.transactions.doctype.outbox_memo.outbox_memo.get_shared_outbox_memos',
                args: {
                    user: frappe.session.user
                },
                callback: function(response) {
                    if (response.message) {
                        const allowed_memos = response.message;
                        listview.filter_area.add([
                            ['Outbox Memo', 'name', 'in', allowed_memos]
                        ]);
    
                        $('.filter-selector').hide();
                    }
                }
            });
        }
    }
};