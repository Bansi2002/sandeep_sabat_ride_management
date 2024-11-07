import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_course_user_counts(filters)    
    return columns, data


def get_columns(filters):
    columns = []
    columns.extend([
        {
            "fieldname": "course",
            "label": _("Course Name"),
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


def get_course_user_counts(filters):
    course_user_counts = []
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    course = filters.get("course")
    completion_from = filters.get("completion_from")
    completion_to = filters.get("completion_to")

    if course:
        courses = frappe.get_all("LMS Enrollment", distinct=True, fields=["course"], filters={'course': filters.get("course")})
    else:
        courses = frappe.get_all("LMS Enrollment", distinct=True, fields=["course"])

    for course in courses:
        course_name = course.get("course")
        
        # Construct the filter conditions
        count_filters = {"course": course_name}
        
        if from_date:
            count_filters["creation"] = [">=", from_date]
        if to_date:
            if "creation" in count_filters:
                count_filters["creation"] = ["between", [from_date, to_date]]
            else:
                count_filters["creation"] = ["<=", to_date]
        
        if completion_from:
            count_filters["completion_date"] = [">=", completion_from]
        if completion_to:
            if "completion_date" in count_filters:
                count_filters["completion_date"] = ["between", [completion_from, completion_to]]
            else:
                count_filters["completion_date"] = ["<=", completion_to]

        user_count = frappe.db.count("LMS Enrollment", filters=count_filters)
        course_user_counts.append({"course": course_name, "user_count": user_count})
    
    return course_user_counts


