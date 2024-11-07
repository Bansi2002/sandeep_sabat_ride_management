import frappe
from lms.lms.md import find_macros
from lms.lms.utils import get_course_progress
from frappe.utils import nowdate

@frappe.whitelist()
def save_progress(lesson, course, status):
	membership = frappe.db.exists(
		"LMS Enrollment", {"member": frappe.session.user, "course": course}
	)
	if not membership:
		return 0

	body = frappe.db.get_value("Course Lesson", lesson, "body")
	macros = find_macros(body)
	quizzes = [value for name, value in macros if name == "Quiz"]

	for quiz in quizzes:
		passing_percentage = frappe.db.get_value("LMS Quiz", quiz, "passing_percentage")
		if not frappe.db.exists(
			"LMS Quiz Submission",
			{
				"quiz": quiz,
				"owner": frappe.session.user,
				"percentage": [">=", passing_percentage],
			},
		):
			return 0

	filters = {"lesson": lesson, "owner": frappe.session.user, "course": course}
	if frappe.db.exists("LMS Course Progress", filters):
		doc = frappe.get_doc("LMS Course Progress", filters)
		doc.status = status
		doc.save(ignore_permissions=True)
	else:
		frappe.get_doc(
			{
				"doctype": "LMS Course Progress",
				"lesson": lesson,
				"status": status,
				"member": frappe.session.user,
			}
		).save(ignore_permissions=True)

	progress = get_course_progress(course)
	frappe.db.set_value("LMS Enrollment", membership, "progress", progress)
	if progress ==100:
		frappe.db.set_value("LMS Enrollment", membership, "completion_date", nowdate())

	return progress