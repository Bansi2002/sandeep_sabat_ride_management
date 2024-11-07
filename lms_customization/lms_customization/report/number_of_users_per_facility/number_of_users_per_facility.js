// Copyright (c) 2024, 8848digital and contributors
// For license information, please see license.txt

frappe.query_reports["Number of users per facility"] = {
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
			fieldname: "branch",
			label: __("Facility"),
			fieldtype: "Link",
			options:"Branch"
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
