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
        data['date'] = time.strftime("%Y-%m-%dT%H:%M:%S") # creation date and time ( e.g. 2010-02-15T07:30:00 )
      
      
      
        #rechnungssteller/biller ist zahnarzt
        biller_details = frappe.get_doc('Healthcare Practitioner', doc.ref_practitioner)
        biller_address = get_primary_address(target_name=doc.ref_practitioner, target_type="Healthcare Practitioner")
         
        data['biller'] = {
            'designation' : biller_details.designation,
            'family_name' : biller_details.first_name,
            'given_name' : biller_details.last_name,
            #'street' : cgi.escape(biller_address.address_line1),  
            'street' : biller_address['address_line1'],
            #statecode aus primary address county genommen, gäbe sicher noich andere richtige lösung aber momentan stimmt das so
            'statecode' : biller_address['county'],
            'zip' : biller_address['pincode'],
            'city' : biller_address['city'],
            'phone' : biller_details.mobile_phone,
            'fax' : biller_address['fax']
            }
            
        #debitor GLEICH wie isnurance
        debitor_details = frappe.get_doc('Patient', doc.patient)
        insurance = frappe.get_doc('Insurance', debitor_details.insurance)
        data['debitor'] = {
            'company' : insurance.company_name,
            'street' : insurance.street,
            'zip' : insurance.pincode, 
            'city' : insurance.city
            }
            
            
            
            
            
            
      

        content = frappe.render_template('spinadent/spinadent/doctype/tarpoints_setting/templateTest.html', data)
        return {'content': content} #returns data
     
        
