# -*- coding: utf-8 -*-
# Copyright (c) 2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

@frappe.whitelist()
def make_tarpoint_file(self):

        data = {}
        data['xml_version'] = frappe.get_value("ERPNextSwiss Settings", "ERPNextSwiss Settings", "xml_version")
        data['xml_region'] = frappe.get_value("ERPNextSwiss Settings", "ERPNextSwiss Settings", "banking_region")
        data['date'] = time.strftime("%Y-%m-%dT%H:%M:%S")                    # creation date and time ( e.g. 2010-02-15T07:30:00 )
      
		#rechnungssteller
        company_address = get_primary_address(target_name=self.company, target_type="Company")
        data['biller'] = {
            #data['biller']['company_name'] = frappe.get_doc('self.doctype', self.company )
            #data['biller']['street'] = cgi.escape(company_address.address_line1)
            #data['biller']['zip'] = cgi.escape(company_address.pincode)
            #data['biller']['city'] = cgi.escape(company_address.city)
            #data['biller']['phone'] = 
        }

        content = frappe.render_template('spinadent/spinadent/doctype/tarpoints_setting/templateTest.html', data) #renders template and data from database
        return {'content': content} #returns data
