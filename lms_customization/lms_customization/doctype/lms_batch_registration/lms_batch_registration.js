// Copyright (c) 2024, 8848digital and contributors
// For license information, please see license.txt

frappe.ui.form.on('LMS Batch Registration', {
    before_submit: function(frm) {
        if (frm.doc.status === 'Approved') {
            console.log('Document is being submitted and status is Approved, proceeding to fetch LMS Batch:', frm.doc.batch);

            frappe.get_doc('LMS Batch', frm.doc.batch)
                .then(batch => {
                    console.log('Fetched LMS Batch:', batch);

                    const student = {
                        student: frm.doc.name, // Assuming 'Name' from LMS Batch Registration should be used as 'student'
                        student_name: frm.doc.user // Assuming 'User' from LMS Batch Registration should be used as 'student_name'
                    };
                    console.log('Prepared student record to add:', student);

                    const new_student_row = frappe.model.add_child(batch, 'Students', 'students');
                    new_student_row.student = student.student;
                    new_student_row.student_name = student.student_name;
                    console.log('Added new student row to LMS Batch:', new_student_row);

                    // Save the updated LMS Batch document
                    frappe.save_doc(batch)
                        .then(() => {
                            console.log('LMS Batch updated successfully with new student');
                        })
                        .catch(err => {
                            console.error('Error saving LMS Batch:', err);
                        });
                })
                .catch(err => {
                    console.error('Error fetching LMS Batch:', err);
                });
        } else {
            console.log('Document is being submitted but status is not Approved, no action taken');
        }
    }
});