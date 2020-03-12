// Copyright (c) 2020, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Note', {
	refresh(frm) {
		// your code here
		 frm.add_custom_button(__("Download Tarpoint File"), function() {
                   generate_tarpoint(frm);
             });
	}
})

function generate_tarpoint(frm) {
     console.log("creating file...");
     frappe.call({
          method: 'spinadent.spinadent.doctype.tarpoints_setting.tarpoints_setting.make_tarpoint_file',
          doc: frm.doc,
          callback: function(r) {
               if (r.message) {
                    // prepare the xml file for download
                    download("tarpoint.xml", r.message.content);
               } 
          }
     });     
}

function download(filename, content) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:application/octet-stream;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.bod
