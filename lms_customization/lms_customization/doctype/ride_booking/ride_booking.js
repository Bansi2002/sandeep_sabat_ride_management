// Copyright (c) 2024, 8848digital and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Ride Booking", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Ride Add On", {
	total_amount(frm,cdt,cdn) {
        var total = 0;
        var d = local[cdt][cdn];
        frm.doc.services.forEcah(function(d){
            total += d.amount;
        })
        var calc = (frm.doc.price_per_km*estimated_km) + total
        frm.set_value("total_amount", calc)
        frm.refresh_field("total_amount")
	},
});