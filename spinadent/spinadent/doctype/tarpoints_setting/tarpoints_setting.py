# -*- coding: utf-8 -*-
# Copyright (c) 2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
import time
from erpnextswiss.erpnextswiss.common_functions import get_building_number, get_street_name, get_pincode, get_city, get_primary_address
import cgi          
import re
    
@frappe.whitelist()
def make_tarpoint_file(qtn=None,so=None, sinv=None, dn=None):
        if dn:
            doc = frappe.get_doc('Delivery Note', dn)
        elif so:
            doc=frappe.get_doc('Sales Order', so)
        elif sinv:
            doc=frappe.get_doc('Sales Invoice', sinv) 
        elif qtn:
            doc=frappe.get_doc('Quotation', qtn) 
        else:
            frappe.throw("Please provide an argument")
            
        data = {}
        data['xml_version'] = frappe.get_value("ERPNextSwiss Settings", "ERPNextSwiss Settings", "xml_version")
        data['xml_region'] = frappe.get_value("ERPNextSwiss Settings", "ERPNextSwiss Settings", "banking_region")
        data['date'] = time.strftime("%Y-%m-%dT%H:%M:%S") 
      
        biller_details = frappe.get_doc('Healthcare Practitioner', doc.ref_practitioner)
        biller_address = get_primary_address(target_name=doc.ref_practitioner, target_type="Healthcare Practitioner")
         
        if biller_details.gln_number:
            practitioner_gln_number = biller_details.gln_number
        else: 
            practitioner_gln_number = "G999999"
        
        data['biller'] = {
            'designation' : biller_details.designation,
            'family_name' : biller_details.first_name,
            'given_name' : biller_details.last_name,
            'street' : biller_address['address_line1'],
            'statecode' : biller_address['county'][:2].upper(),
            'zip' : biller_address['pincode'],
            'city' : biller_address['city'],
            'phone' : biller_details.mobile_phone,
            'fax' : biller_address['fax'],
            'gln_number': practitioner_gln_number,
            'zsr_number' : biller_details.zsr_number,
            #'tax_id' : biller_details.tax_id,
            'subaddressing' : biller_details.department
            }

        debitor_details = frappe.get_doc('Patient', doc.patient)
        insurance = frappe.get_doc('Insurance', debitor_details.insurance)
        
        if insurance.gln_nummer:
            insurance_gln_number = insurance.gln_nummer
        else: 
            insurance_gln_number = "G999999"
        
        data['debitor'] = {
            'company' : insurance.company_name,
            'street' : insurance.street,
            'zip' : insurance.pincode, 
            'city' : insurance.city,
            'gln_nr' : insurance_gln_number
            }
            
        provider_details = frappe.get_doc('Healthcare Practitioner', doc.ref_practitioner)
        provider_address = get_primary_address(target_name=doc.ref_practitioner, target_type="Healthcare Practitioner")
         
        data['provider'] = {
            'designation' : provider_details.designation,
            'family_name' : provider_details.first_name,
            'given_name' : provider_details.last_name,
            'street' : provider_address['address_line1'],
            'statecode' : provider_address['county'][:2].upper(),
            'zip' : provider_address['pincode'],
            'city' : provider_address['city'],
            'phone' : provider_details.mobile_phone,
            'fax' : provider_address['fax'],
            'gln_number': practitioner_gln_number,
            'zsr_number' : provider_details.zsr_number,
            'subaddressing' : provider_details.department
            }    
            
        data['insurance'] = {
            'company' : insurance.company_name,
            'street' : insurance.street,
            'zip' : insurance.pincode, 
            'city' : insurance.city,
            'gln_nr' : insurance.gln_nummer
            }
            
        patient_details = frappe.get_doc('Patient', doc.patient)
        patient_address = get_primary_address(target_name=doc.patient, target_type="Patient")
        
        name = patient_details.patient_name;
        first_name = name.split()[0];
        last_name = name.split()[-1]
        
        if patient_details.sex == "Female":
            salutation = "Frau"
        else:
            salutation = "Herr"
        
        data['patient'] = {
            'gender' : patient_details.sex,
            'birthdate' : patient_details.dob,
            'salutation' : salutation,
            'family_name' : last_name,
            'given_name' : first_name,
            'street' : patient_details.street,
            'country' : patient_details.country,
            'zip' : patient_details.pincode,
            'city' : patient_details.city,
            'ahv_number' : patient_details.ahv_nummer
            }
            
        data['guarantor'] = {
            'salutation' : salutation,
            'family_name' : last_name,
            'given_name' : first_name,
            'street' : patient_details.street,
            'zip' : patient_details.pincode,
            'city' : patient_details.city,
            }
            
        tax_id_toInt = ""  
        if doc.tax_id: 
            t_id = doc.tax_id
            tax_id_toInt = re.sub("[^0-9]", "", t_id)
      
        taxless_amount = (doc.net_total) - (doc.total_taxes_and_charges)
       
        data['balance'] = {
            'currency' : doc.currency,
            'net_total' : doc.net_total,
            'tax_id' : tax_id_toInt,
            'taxless_total' : taxless_amount, 
            'total_taxes' : doc.total_taxes_and_charges 
            } 
              
        creditor_details = frappe.get_doc('Healthcare Practitioner', doc.ref_practitioner)
        creditor_address = get_primary_address(target_name=doc.ref_practitioner, target_type="Healthcare Practitioner")
        data['creditor'] = {
            'designation' : creditor_details.designation,
            'family_name' : creditor_details.first_name,
            'given_name' : creditor_details.last_name,
            'street' : creditor_address['address_line1'],
            'country_code' : creditor_address['country_code'], 
            'zip' : creditor_address['pincode'],
            'city' : creditor_address['city']
            }
          
        data['items'] = {
        'items_table' : doc.items
        }

        if doc.payment_terms_template:
            payment_terms_template = frappe.get_doc("Payment Terms Template", doc.payment_terms_template)
            if payment_terms_template:
                due_period = payment_terms_template.terms[0].credit_days
            else:
                due_period = 30
        else:
            due_period = 30
        
        data['payment_period'] ={
        'py_pr' : "Payment is due within {0} days from invoice date.".format(due_period)
        } 
      
    
        content = frappe.render_template('spinadent/spinadent/doctype/tarpoints_setting/templateTest.html', data)
        return {'content': content}
     
