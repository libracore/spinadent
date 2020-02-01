// Copyright (c) 2019-2020, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sammelrechnung', {
	refresh: function(frm) {
        if ((frm.doc.__islocal) && (!frm.doc.date)) {
            var today = new Date();
            cur_frm.set_value("date", today.toISOString().slice(0, 10));
        }
	},
    restrict_to_customer: function(frm) {
        frappe.call({
            method: 'clear_delivery_notes',
            doc: frm.doc,
            callback: function(response) {
               cur_frm.reload_doc();
            }
        });
    }
});
