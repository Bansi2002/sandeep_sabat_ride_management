// Copyright (c) 2024, 8848digital and contributors
// For license information, please see license.txt

frappe.query_reports["EHC Enrollment with Facility"] = {
	"filters": [

		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "member",
			label: __("Member"),
			fieldtype: "Link",
			options: "User",
		},
		{
			fieldname: "gender",
			label: __("Gender"),
			fieldtype: "Link",
			options: "Gender",
		},
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch",
		},
		{
			fieldname: "job_speciality",
			label: __("Job Speciality"),
			fieldtype: "Link",
			options: "Job Speciality",
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department",
		},
		{
			fieldname: "course",
			label: __("Course"),
			fieldtype: "Link",
			options: "LMS Course",
		},
		{
			fieldname: "from_progress",
			label: __("From Progress"),
			fieldtype: "Int",
		},
		{
			fieldname: "to_progress",
			label: __("To Progress"),
			fieldtype: "Int",
		},
		{
			fieldname: "completion_from",
			label: __(" Completion From Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "completion_to",
			label: __("Completion To Date"),
			fieldtype: "Date",
		},

	]
};
