// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt


frappe.ui.form.on('Study Plan Course', {
    table_ytno_add: function(frm){
        frm.fields_dict['table_ytno'].grid.get_field('course_code').get_query = function(doc){
            var courses_list = [];
            $.each(doc.table_ytno, function(idx, val){
                if (val.course_code) courses_list.push(val.course_code);
            });
            return { filters: [['Course Specification', 'name', 'not in', courses_list]] };
        };
    }
});
