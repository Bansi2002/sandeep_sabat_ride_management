import frappe
from lms.lms.doctype.lms_course.lms_course import can_create_courses
from frappe.utils import cint

@frappe.whitelist(allow_guest=True)
def search_course(text):
	courses = frappe.get_all(
		"LMS Course",
		filters={"published": True},
		or_filters={
			"title": ["like", f"%{text}%"],
			"tags": ["like", f"%{text}%"],
			"short_introduction": ["like", f"%{text}%"],
			"description": ["like", f"%{text}%"],
			"custom_department": ["like", f"%{text}%"],
			"custom_lms_category":["like", f"%{text}%"]
		},
		fields=["name", "title"],
	)
	return courses

@frappe.whitelist()
def save_course(
	tags,
	title,
	short_introduction,
	video_link,
	description,
	course,
	published,
	custom_department,
	custom_lms_category,
	upcoming,
	image=None,
	paid_course=False,
	course_price=None,
	currency=None,
):
	if not can_create_courses(course):
		return

	if course:
		doc = frappe.get_doc("LMS Course", course)
	else:
		doc = frappe.get_doc({"doctype": "LMS Course"})

	doc.update(
		{
			"title": title,
			"short_introduction": short_introduction,
			"video_link": video_link,
			"image": image,
			"description": description,
			"tags": tags,
			"published": cint(published),
			"custom_department": custom_department,
			"custom_lms_category":custom_lms_category,
			"upcoming": cint(upcoming),
			"paid_course": cint(paid_course),
			"course_price": course_price,
			"currency": currency,
		}
	)
	doc.save(ignore_permissions=True)
	return doc.name

@frappe.whitelist(allow_guest=True)
def get_tags(course):
	tags = frappe.db.get_value("LMS Course", course, "tags")
	return tags.split(",") if tags else []

@frappe.whitelist(allow_guest=True)
def get_lesson_count(course):
	lesson_count = 0
	chapters = frappe.get_all("Chapter Reference", {"parent": course}, ["chapter"])
	for chapter in chapters:
		lesson_count += frappe.db.count("Lesson Reference", {"parent": chapter.chapter})

	return lesson_count

@frappe.whitelist(allow_guest=True)
def get_instructors(course):
	instructor_details = []
	instructors = frappe.get_all(
		"Course Instructor", {"parent": course}, order_by="idx", pluck="instructor"
	)
	if not instructors:
		instructors = frappe.db.get_value("LMS Course", course, "owner").split(" ")
	for instructor in instructors:
		instructor_details.append(
			frappe.db.get_value(
				"User",
				instructor,
				["name", "username", "full_name", "user_image"],
				as_dict=True,
			)
		)
	return instructor_details

@frappe.whitelist(allow_guest=True)
def membership(course):
	if frappe.session.user != "Guest":
		membership = frappe.db.get_value("LMS Enrollment",
		{"member": frappe.session.user, "course": course},
		["name", "course", "batch_old", "current_lesson", "member_type", "progress"], as_dict=1)
		if membership:
			progress = frappe.utils.cint(membership.progress)
		else:
			membership, progress = None, None
	else:
		membership, progress = None, None
	return membership, progress

@frappe.whitelist(allow_guest=True)
def get_link_field():
	get_option = []
	get_option.append('')
	meta = frappe.get_meta("LMS Course")
	for field in meta.fields:
		if field.fieldtype == 'Link':
			get_option.append(field.fieldname)

	return get_option

@frappe.whitelist(allow_guest=True)
def get_data_option(data):
	meta = frappe.get_meta("LMS Course")
	for field in meta.fields:
		if field.fieldname == data:
			return field.options
		
@frappe.whitelist(allow_guest=True)
def get_lesson_index(course):
	lesson_name = course
	"""Returns the {chapter_index}.{lesson_index} for the lesson."""
	lesson = frappe.db.get_value(
		"Lesson Reference", {"lesson": lesson_name}, ["idx", "parent"], as_dict=True
	)
	if not lesson:
		return "1.1"

	chapter = frappe.db.get_value(
		"Chapter Reference", {"chapter": lesson.parent}, ["idx"], as_dict=True
	)
	if not chapter:
		return "1.1"

	return f"{chapter.idx}.{lesson.idx}"

