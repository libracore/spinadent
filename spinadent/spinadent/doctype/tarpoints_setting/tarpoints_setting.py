# -*- coding: utf-8 -*-
# Copyright (c) 2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
import time
from erpnextswiss.erpnextswiss.common_functions import get_building_number, get_street_name, get_pincode, get_city, get_primary_address
import cgi          # used to escape xml content
    
@frappe.whitelist()
def make_tarpoint_file(qtn=None,so=None, sinv=None, dn=None):
        if dn:
            doc = frappe.get_doc('Delivery Note', dn)
        elif so:
            doc=frappe.get_doc('Sales order', so)
        elif sinv:
            doc=frappe.get_doc('Sales Invoice', sinv) 
        elif qtn:
            doc=frappe.get_doc('Quotation', qtn) 
        else:
            frappe.throw("Provide an argument")
        data = {}
        data['xml_version'] = frappe.get_value("ERPNextSwiss Settings", "ERPNextSwiss Settings", "xml_version")
        data['xml_region'] = frappe.get_value("ERPNextSwiss Settings", "ERPNextSwiss Settings", "banking_region")
        data['date'] = time.strftime("%Y-%m-%dT%H:%M:%S")                    # creation date and time ( e.g. 2010-02-15T07:30:00 )
      
      
      
        #rechnungssteller
        company = frappe.get_doc('Company', doc.company)
        company_address = get_primary_address(target_name=doc.company, target_type="Company")
        
        if company_address:
            data['biller'] = {
                'company_name' : company.name,
                
                'street' : company_address.address_line1 or "",
                'zip' : cgi.escape(company_address.pincode),
                'city' : cgi.escape(company_address.city),
                
                'phone' : company.phone_no,
                'fax' : company.fax
            }
        else:
            data['biller'] = {
                'company_name' : company.name,
                
                'street' : None,
                'zip' : None,
                'city' : None,
                
				'phone' : company.phone_no,
                'fax' : company.fax
			}
            
        #balance
        #taxes_charges = frappe.get_doc('Sales Taxes and Charges', doc.taxes)
        
            
        data['balance'] = {
            'currency' : doc.currency,
            'total' : doc.total,
            'net_total' : doc.net_total,
            'vat_number' : doc.tax_id,
            'vat' : doc.total_taxes_and_charges,
            #'vat_rate' : taxes_charges.rate,
            'amount' : doc.total_taxes_and_charges
        } 
            
           
        
            
            

        content = frappe.render_template('spinadent/spinadent/doctype/tarpoints_setting/templateTest.html', data)
        return {'content': content} #returns data
     
        
