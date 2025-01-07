frappe.listview_settings['Outbox Memo'] = {
    onload: function() {
        $('.btn-primary').filter(function () {
            return $(this).text().trim() === 'Add Outbox Memo';
        }).hide();
    }
};