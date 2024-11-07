import frappe
from frappe.query_builder import DocType
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data

def get_columns():
    columns = [
        {
            "fieldname": "member_email",
            "label": _("Member Email"),
            "fieldtype": "Link",
            "options": "User",
            "width": 135,
        },
        {
            "fieldname": "member_name",
            "label": _("Member Name"),
            "fieldtype": "Data",
            "width": 135,
        },
        {
            "fieldname": "gender",
            "label": _("Gender"),
            "fieldtype": "Link",
            "options": "Gender",
            "width": 135,
        },
        {
            "fieldname": "branch",
            "label": _("Branch"),
            "fieldtype": "Link",
            "options": "Branch",
            "width": 135,
        }, 
        {
            "fieldname": "job_speciality",
            "label": _("Job Speciality"),
            "fieldtype": "Link",
            "options": "Job Speciality",
            "width": 135,
        },
        {
            "fieldname": "department",
            "label": _("Department"),
            "fieldtype": "Link",
            "options": "Department",
            "width": 135,
        }, 
        {
            "fieldname": "course",
            "label": _("Course"),
            "fieldtype": "Link",
            "options": "LMS Course",
            "width": 135,
        },
        {
            "fieldname": "course_name",
            "label": _("Course Name"),
            "fieldtype": "Data",
            "width": 135,
        },
        {
            "fieldname": "current_lesson",
            "label": _("Current Lesson"),
            "fieldtype": "Link",
            "options": "Course Lesson",
            "width": 135,
        },
        {
            "fieldname": "progress",
            "label": _("Progress"),
            "fieldtype": "Data",
            "width": 135,
        },
        {
            "fieldname": "completion_date",
            "label": _("Course Completion Date"),
            "fieldtype": "Date",
            "width": 135,
        },
    ]
    return columns

def get_data(filters):
    LMS_Enrollment = DocType("LMS Enrollment")
    Employee = DocType("Employee")
    Department = DocType("Department")

    query = (
        frappe.qb.from_(LMS_Enrollment)
        .left_join(Employee)
        .on(LMS_Enrollment.member == Employee.company_email)
        .left_join(Department)
        .on((Department.department_id + " - EHC") == Employee.department)
        .select(
            LMS_Enrollment.course.as_("creation"),
            LMS_Enrollment.member.as_("member_email"),
            LMS_Enrollment.member_name.as_("member_name"),
            Employee.gender.as_("gender"),
            Employee.branch.as_("branch"),
            Employee.job_speciality.as_("job_speciality"),
            Employee.department.as_("department"),
            LMS_Enrollment.course.as_("course"),
            LMS_Enrollment.course_name.as_("course_name"),
            LMS_Enrollment.completion_date.as_("completion_date"),
            LMS_Enrollment.current_lesson.as_("current_lesson"),
            LMS_Enrollment.progress.as_("progress")
        )
    )
    if filters.get("from_date") and filters.get("to_date"):
        query = query.where(LMS_Enrollment.creation.between(filters["from_date"], filters["to_date"]))
    elif filters.get("from_date"):
        query = query.where(LMS_Enrollment.creation >= filters["from_date"])
    elif filters.get("to_date"):
        query = query.where(LMS_Enrollment.creation <= filters["to_date"])

    if filters.get("member"):
        query = query.where(LMS_Enrollment.member == filters["member"])
    if filters.get("gender"):
        query = query.where(Employee.gender == filters["gender"])
    if filters.get("branch"):
        query = query.where(Employee.branch == filters["branch"])
    if filters.get("job_speciality"):
        query = query.where(Employee.job_speciality == filters["job_speciality"])
    if filters.get("department"):
        query = query.where(Employee.department == filters["department"])
    if filters.get("course"):
        query = query.where(LMS_Enrollment.course == filters["course"])
    if filters.get("from_progress") and filters.get("to_progress"):
        query = query.where(LMS_Enrollment.progress.between(filters["from_progress"], filters["to_progress"]))
    elif filters.get("from_progress"):
        query = query.where(LMS_Enrollment.progress >= filters["from_progress"])
    elif filters.get("to_progress"):
        query = query.where(LMS_Enrollment.progress <= filters["to_progress"])
    
    if filters.get("completion_from") and filters.get("completion_to"):
        query = query.where(LMS_Enrollment.completion_date.between(filters["completion_from"], filters["completion_to"]))
    elif filters.get("completion_from"):
        query = query.where(LMS_Enrollment.completion_date >= filters["completion_from"])
    elif filters.get("completion_to"):
        query = query.where(LMS_Enrollment.completion_date <= filters["completion_to"])


    data = query.run(as_dict=True)
    return data
