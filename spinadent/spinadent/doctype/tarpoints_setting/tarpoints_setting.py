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
            frappe.throw("Fuck u")
            
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
            
            
        #provider gleich wie biller
        provider_details = frappe.get_doc('Healthcare Practitioner', doc.ref_practitioner)
        provider_address = get_primary_address(target_name=doc.ref_practitioner, target_type="Healthcare Practitioner")
         
        data['provider'] = {
            'designation' : provider_details.designation,
            'family_name' : provider_details.first_name,
            'given_name' : provider_details.last_name,
            'street' : provider_address['address_line1'],
            #statecode aus primary address county genommen, gäbe sicher noich andere richtige lösung aber momentan stimmt das so
            'statecode' : provider_address['county'],
            'zip' : provider_address['pincode'],
            'city' : provider_address['city'],
            'phone' : provider_details.mobile_phone,
            'fax' : provider_address['fax']
            }    
            
            
        #debitor GLEICH wie insurance -> greift auf gleichen doctype zu
        data['insurance'] = {
            'company' : insurance.company_name,
            'street' : insurance.street,
            'zip' : insurance.pincode, 
            'city' : insurance.city
            }
            
            
        #patient GLEICH wie guarantor aber MIT sex und geburtsdatum
        patient_details = frappe.get_doc('Patient', doc.patient)
        patient_address = get_primary_address(target_name=doc.patient, target_type="Patient")
        
        name = patient_details.patient_name;
        first_name = name.split()[0];
        last_name = name.split()[-1]
        
        
        data['patient'] = {
            'gender' : patient_details.sex,
            'birthdate' : patient_details.dob,
            #'salutation' : xxx; patient misses salutation
            'family_name' : last_name,
            'given_name' : first_name,
            
            #patient misses whole address section
            
            #'street' : patient_address['address_line1'],
            #'country' : patient_address['county'],
            #'zip' : patient_address['pincode'],
            #'city' : patient_address['city']
            }
            
            
            
            
        #guarantor GLEICH wie patient aber OHNE sex und geburtsdatum und country
     
        data['guarantor'] = {
            #'salutation' : xxx; guarantor/patient misses salutation
            'family_name' : last_name,
            'given_name' : first_name,
            
            #guerantor/patient misses whole address section
            
            #'street' : patient_address['address_line1'],
            #'zip' : patient_address['pincode'],
            #'city' : patient_address['city']
            }
            
            
    
            
            
            
      

        content = frappe.render_template('spinadent/spinadent/doctype/tarpoints_setting/templateTest.html', data)
        return {'content': content} #returns data
     
        
