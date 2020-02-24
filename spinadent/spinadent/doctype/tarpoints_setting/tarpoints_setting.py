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
        elif dn:
            doc=frappe.get_doc('Delivery Note', dn) 
            
        data = {}
        data['xml_version'] = frappe.get_value("ERPNextSwiss Settings", "ERPNextSwiss Settings", "xml_version")
        data['xml_region'] = frappe.get_value("ERPNextSwiss Settings", "ERPNextSwiss Settings", "banking_region")
        data['date'] = time.strftime("%Y-%m-%dT%H:%M:%S")                    # creation date and time ( e.g. 2010-02-15T07:30:00 )
      
      
      
        #rechnungssteller
        company = frappe.get_doc('Company', doc.company)
        company_address = get_primary_address(doc.company, target_type="Company")
        data['biller'] = {
        # zu doppelpunkt ändern
            'company_name' : company.name,
            'street' : cgi.escape(company_address.address_line1),
            'zip' : cgi.escape(company_address.pincode),
            'city' : cgi.escape(company_address.city),
            #data['biller']['phone'] = 
        }

        customer = frappe.get_doc('Customer', doc.customer)
        customer_address = get_primary_address(target_name=doc.customer, target_type="Customer")
		#rechnungserhalter
        data['customer'] = {
            'family_name' : customer.customer_name,
            'given_name' : customer.customer_name,
            'street' : cgi.escape(customer_address.address_line1),
            'country' : cgi.escape(customer_address.country),
            'zip' : cgi.escape(customer_address.pincode),
            'city' : cgi.escape(customer_address.city)
        }
        
        #patient
        patient = frappe.get_doc('Patient', doc.patient)
        patient_adress = get_primary_address(target_name=doc.patient, target_type="Patient")
        data['patient'] = {
            'birthday' : patient.dob,
            'gender' :  patient.sex,
            'family_name' :  patient.patient_name,
            'street' : cgi.escape(patient_adress.address_line1),
            'country' : cgi.escape(patient_adress.country),
            'zip' : cgi.escape(patient_adress.pincode),
            'city' : cgi.escape(patient_adress.city)
        }     


#richtiges template nch eibbinden
        content = frappe.render_template('erpnextswiss/spinadent/doctype/tarpoint_setting/templateTest.html', data) #renders template and data from database
        return {'content': content} #returns data
     
           
        #richtiges template nch eibbinden
        content = frappe.render_template('erpnextswiss/spinadent/doctype/tarpoint_setting/templateTest.html', data) #renders template and data from database
        return {'content': content}

