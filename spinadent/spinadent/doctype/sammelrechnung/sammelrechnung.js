// Copyright (c) 2019, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sammelrechnung', {
	refresh: function(frm) {
        if ((frm.doc.__islocal) && (!frm.doc.date)) {
            var today = new Date();
            cur_frm.set_value("date", today.toISOString().slice(0, 10));
        }
	}
});
