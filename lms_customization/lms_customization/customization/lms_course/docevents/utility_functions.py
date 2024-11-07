import frappe
from jinja2 import Template

@frappe.whitelist()
def send_emails(user_ids, course_name):
    if isinstance(user_ids, str):
        user_ids = frappe.parse_json(user_ids)
    
    doc = frappe.get_doc("LMS Course", course_name)

    template = frappe.get_value("LMS Settings", "LMS Settings", "course_updation")
    if template:
        subject = frappe.get_value("Email Template", template, "subject")
        message = frappe.get_value("Email Template", template, "response")
        doc_attrs = {attr: getattr(doc, attr) for attr in dir(doc) if not attr.startswith('_') and not callable(getattr(doc, attr))}
        jinja_template = Template(message)
        formatted_message = jinja_template.render(doc_attrs)
        for email in user_ids:
            if email:
                frappe.sendmail(recipients=email, subject=subject, message=formatted_message)
        return "Email sent successfully"
    else:
        return "Select Email Template in LMS Settings"

@frappe.whitelist()
def user_role_check(user):
    roles = frappe.get_roles(user)
    for role in roles:
        if role == "LMS Student":
            return 1
        else:
            return 0
    