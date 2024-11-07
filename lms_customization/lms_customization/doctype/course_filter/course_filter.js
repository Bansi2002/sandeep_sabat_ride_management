frappe.ui.form.on('Course Filter', {
    refresh: function(frm) {
        console.log(frm.doc)
        frappe.call({
            method: 'lms_customization.lms_customization.customization.lms_course.search_filter.get_link_field',
            callback: function(response) {
                // Clear existing options and add new options
                frappe.meta.get_docfield('Filter Item', 'field', frm.doc.name1).options = (response.message).join('\n');      
                // Refresh the field to display the new options
                frm.refresh_field('department');
            }
        });
    }
});

frappe.ui.form.on('Filter Item', {
    field: function(frm, cdt, cdn){
        var field_value = locals[cdt][cdn].field;
        frappe.call({
            method: 'lms_customization.lms_customization.customization.lms_course.search_filter.get_data_option',
            args:{
                'data': field_value
            },
            callback: function(response) {
                // Handle the response from the server
                frappe.model.set_value(cdt, cdn, 'name1', response.message);
            }
        });
    }

})
