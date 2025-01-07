frappe.listview_settings['Specific Transaction Document'] = {
    onload: function() {
        $('.btn-primary').filter(function () {
            return $(this).text().trim() === 'Add Specific Transaction Document';
        }).hide();
    }
};