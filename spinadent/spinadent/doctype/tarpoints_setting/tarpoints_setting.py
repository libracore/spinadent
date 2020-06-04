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
import cgi              # for string escaping
import re               # to convert tax_ids  
from lxml import etree  # for xml validation
from bs4 import BeautifulSoup	# to remove html tags

@frappe.whitelist()
def make_tarpoint_file(qtn=None,so=None, sinv=None, dn=None, validate=True):
	# load original document
    if dn:
        doc = frappe.get_doc('Delivery Note', dn)
        date = doc.transaction_date
        customer = frappe.get_doc("Customer", doc.customer)
        customer_address = frappe.get_doc("Address", doc.customer_address)
    elif so:
        doc=frappe.get_doc('Sales Order', so)
        date = doc.transaction_date
        customer = frappe.get_doc("Customer", doc.customer)
        customer_address = frappe.get_doc("Address", doc.customer_address)
    elif sinv:
        doc=frappe.get_doc('Sales Invoice', sinv)  
        date = doc.posting_date
        customer = frappe.get_doc("Customer", doc.customer)
        customer_address = frappe.get_doc("Address", doc.customer_address)  
    elif qtn:
        doc=frappe.get_doc('Quotation', qtn)  
        date = doc.transaction_date    
        customer = frappe.get_doc("Customer", doc.party_name) 
        customer_address = frappe.get_doc("Address", doc.customer_address)     
    else:
        frappe.throw("Please provide an argument")

    # collect information
    biller_details = frappe.get_doc('Company', doc.company)
    biller_address = get_primary_address(target_name=doc.company, target_type="Company")
    if not biller_address:
        frappe.throw( _("Please define an address for Company {0}").format(doc.company))

    if not doc.patient:
        frappe.throw( _("Please define an patient for Quotation {0}").format(doc.name))
    debitor_details = frappe.get_doc('Patient', doc.patient)
    if not debitor_details.insurance:
        frappe.throw( _("Please define an insurance for Patient {0}").format(doc.patient))
    insurance = frappe.get_doc('Insurance', debitor_details.insurance)

    provider_details = frappe.get_doc('Healthcare Practitioner', doc.ref_practitioner)
    provider_address = get_primary_address(target_name=doc.ref_practitioner, target_type="Healthcare Practitioner")
    if not provider_address:
        frappe.throw( _("Please define an address for Healthcare Practitioner {0}").format(doc.ref_practitioner))
    if not provider_details.office_phone:
        frappe.throw( _("Please define an office phone number for Healthcare Practitioner {0}").format(doc.ref_practitioner))
    
    if not customer_address.phone:
        frappe.throw( _("Please define a phone number for Address {0}").format(customer_address.name))
    patient_details = frappe.get_doc('Patient', doc.patient)
    patient_address = get_primary_address(target_name=doc.patient, target_type="Patient")
    
    name = patient_details.patient_name;
    first_name = name.split()[0];
    last_name = name.split()[-1]
    
    if patient_details.sex == "Female":
        salutation = "Frau"
    else:
        salutation = "Herr"

    tax_id_toInt = ""  
    if doc.tax_id: 
        t_id = doc.tax_id
        tax_id_toInt = re.sub("[^0-9]", "", t_id)
  
    taxless_amount = (doc.net_total) - (doc.total_taxes_and_charges)

    creditor_details = frappe.get_doc('Healthcare Practitioner', doc.ref_practitioner)
    creditor_address = get_primary_address(target_name=doc.ref_practitioner, target_type="Healthcare Practitioner")
    
    if doc.payment_terms_template:
        payment_terms_template = frappe.get_doc("Payment Terms Template", doc.payment_terms_template)
        if payment_terms_template:
            due_period = payment_terms_template.terms[0].credit_days
        else:
            due_period = 30
    else:
        due_period = 30       

    if patient_details.ahv_nr:
        patient_ahv_nr = re.sub("[^0-9]", "", patient_details.ahv_nr)
    else:
        frappe.throw( _("Please define an AHV number for Patient {0}").format(doc.patient))
    if patient_details.dob:
        patient_dob = patient_details.dob.strftime("%Y-%m-%dT%H:%M:%S") or ""
    else:
        frappe.throw( _("Please define a birth date for Patient {0}").format(doc.patient))
    if doc.terms:
        remarks = BeautifulSoup(doc.terms, "lxml").text
    else:
        remarks = "Keine Anmerkungen"
    
    # create data record
    data = {
        'date': date.strftime("%Y-%m-%dT%H:%M:%S") or "2020-01-01T00:00:00",
        'timestamp': int(time.time()),
        'name': doc.name,
        'title': doc.title,
        'payment_period': "Payment is due within {0} days from invoice date.".format(due_period),
        'remark': cgi.escape(remarks),
        'place': biller_details.tarpoint_place,
        'role': biller_details.tarpoint_role,
        'customer': {
            'title' : cgi.escape(customer.name),
            'family_name' : cgi.escape(customer.customer_name),
            'given_name' : "-", 
            'street' : cgi.escape(customer_address.get('address_line1', '')),
            'statecode' : None, #biller_address.get('county', 'SG')[:2].upper(),
            'zip' : cgi.escape(customer_address.get('pincode', '9000')),
            'city' : cgi.escape(customer_address.get('city', 'Berschis')),
            'phone' : cgi.escape(customer_address.phone),
            'fax' : None,
            'url': cgi.escape(customer.website),
            'email': cgi.escape(customer.email_id),
            'gln_number': cgi.escape(customer.gln_number or "2000000000000"),
            'zsr_number' : cgi.escape(provider_details.zsr_number or "G999999")
        },
        'biller': {
            'designation' : "",
            'family_name' : cgi.escape(doc.company),
            'given_name' : "-", 
            'street' : cgi.escape(biller_address.get('address_line1', '')),
            'statecode' : None, #biller_address.get('county', 'SG')[:2].upper(),
            'zip' : cgi.escape(biller_address.get('pincode', '9000')),
            'city' : cgi.escape(biller_address.get('city', 'Berschis')),
            'phone' : cgi.escape(biller_details.phone_no or ""),
            'fax' : "",
            'gln_number': cgi.escape(biller_details.gln_number or "2000000000000"),
            'zsr_number' : cgi.escape(biller_details.zsr_number or "G999999"),
            'tax_id' : cgi.escape(biller_details.tax_id or ""),
            'subaddressing' : ""
        },
        'debitor': {
            'company' : cgi.escape(insurance.company_name or ""),
            'street' : cgi.escape(insurance.street or ""),
            'zip' : cgi.escape(insurance.pincode or ""), 
            'city' : cgi.escape(insurance.city or ""),
            'gln_nr' : cgi.escape(insurance.gln_nummer or "2000000000000")
        },
        'provider': {
            'title': cgi.escape(provider_details.name[:35]),
            'designation' : cgi.escape(provider_details.designation or ""),
            'family_name' : cgi.escape(provider_details.first_name or ""),
            'given_name' : cgi.escape(provider_details.last_name or ""),
            'street' : cgi.escape(provider_address.get('address_line1', "")),
            'statecode' : None, #provider_address.get('county', "SG")[:2].upper(),
            'zip' : cgi.escape(provider_address.get('pincode', "")),
            'city' : cgi.escape(provider_address.get('city', "")),
            'phone' : cgi.escape(provider_details.office_phone or ""),
            'fax' : provider_address.get('fax', None),
            'gln_number': cgi.escape(provider_details.gln_number or "2000000000000"),
            'zsr_number' : cgi.escape(provider_details.zsr_number or "G999999"),
            'subaddressing' : cgi.escape(provider_details.department or "")
        }, 
        'insurance': {
            'company' : cgi.escape(insurance.company_name or ""),
            'street' : cgi.escape(insurance.street or ""),
            'zip' : cgi.escape(insurance.pincode or ""), 
            'city' : cgi.escape(insurance.city or ""),
            'gln_nr' : cgi.escape(insurance.gln_nummer or "2000000000000")
        },
        'patient': {
            'gender' : patient_details.sex.lower() if patient_details.sex else "female",
            'birthdate' : patient_dob,
            'salutation' : salutation,
            'family_name' : cgi.escape(last_name),
            'given_name' : cgi.escape(first_name),
            'street' : cgi.escape(patient_details.street or ""),
            'country' : cgi.escape(patient_details.country or ""),
            'zip' : cgi.escape(patient_details.pincode or ""),
            'city' : cgi.escape(patient_details.city or ""),
            'ahv_number' : patient_ahv_nr
        },
        'guarantor': {
            'salutation' : salutation,
            'family_name' : cgi.escape(last_name),
            'given_name' : cgi.escape(first_name),
            'street' : cgi.escape(patient_details.street or ""),
            'zip' : cgi.escape(patient_details.pincode or ""),
            'city' : cgi.escape(patient_details.city or ""),
        },
        'items': doc.items,
        'balance': {
            'currency' : doc.currency or "",
            'net_total' : doc.net_total or "",
            'tax_id' : tax_id_toInt,
            'taxless_total' : taxless_amount, 
            'total_taxes' : doc.total_taxes_and_charges or ""
        },
        'creditor': {
            'designation' : cgi.escape(creditor_details.designation or ""),
            'family_name' : cgi.escape(creditor_details.first_name or ""),
            'given_name' : cgi.escape(creditor_details.last_name or ""),
            'street' : cgi.escape(creditor_address['address_line1']),
            'country_code' : cgi.escape(creditor_address['country_code']), 
            'zip' : cgi.escape(creditor_address['pincode']),
            'city' : cgi.escape(creditor_address['city'])
        },
        'treatment': {
            'reason' : cgi.escape(doc.behandlungsgrund or ""),
            'diagnosis' : cgi.escape(doc.diagnose or ""),
            'canton': doc.behandlungskanton or "",
            'begin_date': doc.beginn_behandlung.strftime("%Y-%m-%dT%H:%M:%S") or "2020-01-01T00:00:00"
        },
        'accident_details': {
            'accident_date' : (doc.fall_unfalldatum).strftime("%Y-%m-%dT%H:%M:%S") or "2020-01-01T00:00:00",
            'accident_id' : cgi.escape(doc.fall_nr_versicherung_ or "G999999")
        }
    }

    # render data into template
    if qtn:
        content = frappe.render_template('spinadent/spinadent/doctype/tarpoints_setting/quotation.html', data)
    else:
        content = frappe.render_template('spinadent/spinadent/doctype/tarpoints_setting/invoice.html', data)
    
    # validate xml content
    if validate:
        # load schema
        base_path = frappe.get_app_path("spinadent")
        if qtn:
            schema_file = base_path + "/public/xsd/generalCreditRequest_430.xsd"
        else:
            schema_file = base_path + "/public/xsd/generalCreditRequest_430.xsd"
        
        xsd_root = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xsd_root)
        
        # parse content
        xml_root = etree.fromstring(content.encode('utf-8'))
        # validate
        if not xmlschema.validate(xml_root):
            frappe.throw( _("Failed to validate content: {0}").format(xmlschema.error_log.last_error))
    
    # return xml content
    return {'content': content}
 
