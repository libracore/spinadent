# -*- coding: utf-8 -*-
# Copyright (c) 2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime, timedelta
import time
from erpnextswiss.erpnextswiss.common_functions import get_building_number, get_street_name, get_pincode, get_city, get_primary_address
import cgi
import re
    
@frappe.whitelist()
def make_tarpoint_file(qtn=None,so=None, sinv=None, dn=None):
	# load original document
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
    
    # create data record
    data = {}	
    data['date'] = time.strftime("%Y-%m-%dT%H:%M:%S") 
  
    biller_details = frappe.get_doc('Company', doc.company)
    biller_address = get_primary_address(target_name=doc.company, target_type="Company")
    if not biller_address:
        frappe.throw( _("Please define an address for Company {0}").format(doc.company))
        
    data['biller'] = {
        'designation' : "",
        'family_name' : doc.company,
        'given_name' : "", 
        'street' : biller_address.get('address_line1', ''),
        'statecode' : None, #biller_address.get('county', 'SG')[:2].upper(),
        'zip' : biller_address.get('pincode', '9000'),
        'city' : biller_address.get('city', 'Berschis'),
        'phone' : biller_details.phone_no or "",
        'fax' : "",
        'gln_number': biller_details.gln_number or "2000000000000",
        'zsr_number' : biller_details.zsr_number or "G999999",
        'tax_id' : biller_details.tax_id or "",
        'subaddressing' : ""
        }

    debitor_details = frappe.get_doc('Patient', doc.patient)
    insurance = frappe.get_doc('Insurance', debitor_details.insurance)
    
    if insurance.gln_nummer:
        insurance_gln_number = insurance.gln_nummer
    else: 
        insurance_gln_number = "G999999"
    
    data['debitor'] = {
        'company' : insurance.company_name or "",
        'street' : insurance.street or "",
        'zip' : insurance.pincode or "", 
        'city' : insurance.city or "",
        'gln_nr' : insurance_gln_number or ""
        }
        
    provider_details = frappe.get_doc('Healthcare Practitioner', doc.ref_practitioner)
    provider_address = get_primary_address(target_name=doc.ref_practitioner, target_type="Healthcare Practitioner")
    if not provider_address:
        frappe.throw( _("Please define an address for Healthcare Practitioner {0}").format(doc.ref_practitioner))
        
    data['provider'] = {
        'designation' : provider_details.designation or "",
        'family_name' : provider_details.first_name or "",
        'given_name' : provider_details.last_name or "",
        'street' : provider_address.get('address_line1', ""),
        'statecode' : None, #provider_address.get('county', "SG")[:2].upper(),
        'zip' : provider_address.get('pincode', ""),
        'city' : provider_address.get('city', ""),
        'phone' : provider_details.mobile_phone or "",
        'fax' : provider_address.get('fax', ""),
        'gln_number': provider_details.gln_number or "2000000000000",
        'zsr_number' : provider_details.zsr_number or "G999999",
        'subaddressing' : provider_details.department or "",
        'role' : provider_details.department or "",
        'place' : provider_details.designation or ""
        }    
        
    data['insurance'] = {
        'company' : insurance.company_name or "",
        'street' : insurance.street or "",
        'zip' : insurance.pincode or "", 
        'city' : insurance.city or "",
        'gln_nr' : insurance.gln_nummer or ""
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
        'gender' : patient_details.sex or "",
        'birthdate' : patient_details.dob or "",
        'salutation' : salutation,
        'family_name' : last_name,
        'given_name' : first_name,
        'street' : patient_details.street or "",
        'country' : patient_details.country or "",
        'zip' : patient_details.pincode or "",
        'city' : patient_details.city or "",
        'ahv_number' : patient_details.ahv_nr or "G999999"
        }
        
    data['guarantor'] = {
        'salutation' : salutation,
        'family_name' : last_name,
        'given_name' : first_name,
        'street' : patient_details.street or "",
        'zip' : patient_details.pincode or "",
        'city' : patient_details.city or "",
        }
        
    tax_id_toInt = ""  
    if doc.tax_id: 
        t_id = doc.tax_id
        tax_id_toInt = re.sub("[^0-9]", "", t_id)
  
    taxless_amount = (doc.net_total) - (doc.total_taxes_and_charges)
   
    data['balance'] = {
        'currency' : doc.currency or "",
        'net_total' : doc.net_total or "",
        'tax_id' : tax_id_toInt,
        'taxless_total' : taxless_amount, 
        'total_taxes' : doc.total_taxes_and_charges or ""
        } 
          
    creditor_details = frappe.get_doc('Healthcare Practitioner', doc.ref_practitioner)
    creditor_address = get_primary_address(target_name=doc.ref_practitioner, target_type="Healthcare Practitioner")
    data['creditor'] = {
        'designation' : creditor_details.designation or "",
        'family_name' : creditor_details.first_name or "",
        'given_name' : creditor_details.last_name or "",
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
  
    
    data['diagnosis_details'] = {
        'reason' : doc.behandlungsgrund or "",
        'diagnosis' : doc.diagnose or ""
    }
    
    
    data['accident_details'] = {
        'accident_date' : (doc.fall_unfalldatum).strftime("%Y-%m-%d") or "2020-01-01",
        'accident_id' : doc.fall_nr_versicherung_ or "G999999"
    }
    
    data['title'] = {
        'doc_title' : doc.title
    }

    if dn:
        data['invoice'] = {
            'details' : (doc.transaction_date).strftime("%Y-%m-%d") or "2020-01-01",
        }
    elif so:
        data['invoice'] = {
            'details' : (doc.transaction_date).strftime("%Y-%m-%d") or "2020-01-01",
        }
    elif sinv:
        data['invoice'] = {
            'details' : (doc.posting_date).strftime("%Y-%m-%d") or "2020-01-01",
        }             
    elif qtn:
        data['invoice'] = {
            'details' : (doc.transaction_date).strftime("%Y-%m-%d") or "2020-01-01",
        }            
    else:
        data['invoice'] = {
            'details' : "2020-01-01",
        } 

    # render data into template
    if qtn:
        content = frappe.render_template('spinadent/spinadent/doctype/tarpoints_setting/quotation.html', data)
    else:
        content = frappe.render_template('spinadent/spinadent/doctype/tarpoints_setting/invoice.html', data)
    # return xml content
    return {'content': content}
 
