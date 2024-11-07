import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_department_user_counts(filters)
    return columns, data


def get_columns(filters):
    columns = []
    columns.extend([
            {
                "fieldname": "department",
                "label": _("Department Name"),
                "fieldtype": "Data",
                "width": 250,
            },
            {
                "fieldname": "user_count",
                "label": _("Total Users"),
                "fieldtype": "Int",
                "width": 250,
            }
        ])
   
    return columns


def get_department_user_counts(filters):
    department_user_counts = []
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    department_filter = filters.get("department")
    completion_from = filters.get("completion_from")
    completion_to = filters.get("completion_to")
    enrollment_filters = {}
    if from_date:
        enrollment_filters["creation"] = [">=", from_date]
    if to_date:
        if "creation" in enrollment_filters:
            enrollment_filters["creation"] = ["between", [from_date, to_date]]
        else:
            enrollment_filters["creation"] = ["<=", to_date]

    if completion_from:
        enrollment_filters["completion_date"] = [">=", completion_from]
    if completion_to:
        if "completion_date" in enrollment_filters:
            enrollment_filters["completion_date"] = ["between", [completion_from, completion_to]]
        else:
            enrollment_filters["completion_date"] = ["<=", completion_to]

    enrollments = frappe.get_all("LMS Enrollment", filters=enrollment_filters, fields=["member"])

    for enrollment in enrollments:
        user_id = enrollment.get("member")
        employee = frappe.get_value("Employee", {"company_email": user_id}, ["name", "department"])
        if employee and employee[1]: 
            department_name = employee[1]
            if department_filter and department_name not in department_filter:
                continue
            department_exists = False
            for department_count in department_user_counts:
                if department_count["department"] == department_name:
                    department_count["user_count"] += 1
                    department_exists = True
                    break
            if not department_exists:
                department_user_counts.append({"department": department_name, "user_count": 1})

    return department_user_counts
