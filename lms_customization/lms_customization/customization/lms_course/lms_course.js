frappe.ui.form.on('LMS Course', {
    refresh: function(frm) {
        if (!frm.is_new()) { // Check if the document is not new
            frm.add_custom_button(__('Send Email'), function() {
                if (frm.doc.custom_department) {
                    frappe.call({
                        method: 'frappe.client.get_list',
                        args: {
                            doctype: 'Employee',
                            filters: {
                                department: frm.doc.custom_department
                            },
                            fields: ['user_id']
                        },
                        callback: function(r) {
                            if (r.message && r.message.length > 0) {
                                let user_ids = r.message.map(emp => emp.user_id);
                                send_email_notifications(user_ids, frm);
                            } else {
                                frappe.msgprint(__('No employees found in the specified department'));
                            }
                        }
                    });
                } else {
                    frappe.msgprint(__('Please specify a department'));
                }
            }).addClass('btn-primary');
        }
    }
});

function send_email_notifications(user_ids, frm) {
    frappe.call({
        method: 'lms_customization.lms_customization.customization.lms_course.docevents.utility_functions.send_emails',
        args: {
            user_ids: user_ids,
            course_name: frm.doc.name
        },
        callback: function (r) {
            if (r.message) {
                frappe.msgprint(__(r.message));
            }
        }
    });
}
