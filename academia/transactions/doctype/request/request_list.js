frappe.listview_settings['Request'] = {
    onload: function() {
        $('.btn-primary').filter(function () {
            return $(this).text().trim() === 'Add Request';
        }).hide();
    }
};