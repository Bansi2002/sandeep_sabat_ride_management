import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_branch_user_counts(filters)

    return columns, data


def get_columns(filters):
    columns = []
    columns.extend([
            {
                "fieldname": "branch",
                "label": _("Facility Name"),
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
def get_branch_user_counts(filters):
    branch_user_counts = []
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    branch = filters.get("branch")
    completion_from = filters.get("completion_from")
    completion_to = filters.get("completion_to")

    # Construct the filter conditions for enrollments
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

    # Get enrollments with the specified filters
    enrollments = frappe.get_all("LMS Enrollment", filters=enrollment_filters, fields=["member"])
    
    for enrollment in enrollments:
        user_id = enrollment.get("member")
        employee = frappe.get_value("Employee", {"company_email": user_id}, ["name", "branch"])
        if employee and employee[1]:
            branch_name = employee[1]
            if branch and branch_name != branch:
                continue  # Skip this employee if the branch does not match the filter
            
            branch_exists = False
            for branch_count in branch_user_counts:
                if branch_count["branch"] == branch_name:
                    branch_count["user_count"] += 1
                    branch_exists = True
                    break
            if not branch_exists:
                branch_user_counts.append({"branch": branch_name, "user_count": 1})
                
    return branch_user_counts

