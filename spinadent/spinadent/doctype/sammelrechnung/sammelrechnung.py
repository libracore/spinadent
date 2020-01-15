# -*- coding: utf-8 -*-
# Copyright (c) 2019-2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Sammelrechnung(Document):
    def validate(self):
        pass
        
    def before_save(self):
        # run this before saving
        if not self.delivery_notes:
            self.collect_values() 
        return
        
    def on_submit(self):
        # create collected sales invoices
        self.create_sales_invoices()
        return
    
    def on_cancel(self):
        # unlink delivery notes, cancel sales invoices
        self.unlink_docs()
        return
            
    def collect_values(self):               
        sql_query = """SELECT 
                `tabDelivery Note`.`name`,
                `tabDelivery Note`.`customer`,
                `tabDelivery Note`.`customer_name`
            FROM `tabDelivery Note`
            WHERE 
                `tabDelivery Note`.`docstatus` = 1 /* only valid documents */
                AND `tabDelivery Note`.`sammelrechnung` IS NULL /* only documents that have not been invoiced */;
        """
        delivery_notes = frappe.db.sql(sql_query, as_dict=True)
        
        self.delivery_notes = []
        for delivery_note in delivery_notes:
            row = self.append('delivery_notes', {
                'delivery_note': delivery_note['name'], 
                'customer': delivery_note['customer'],
                'customer_name': delivery_note['customer_name'],
            })
        return

    def create_sales_invoices(self):
        # collect list of customers (to aggregate)
        customers = []
        for delivery_note in self.delivery_notes:
            if delivery_note.customer not in customers:
                customers.append(delivery_note.customer)
        # create sales invoices based on delivery note
        self.sales_invoices = []
        for customer in customers:
            new_sinv = frappe.get_doc({
                'doctype': 'Sales Invoice'
            })
            customer_name = ""
            for delivery_note in self.delivery_notes:
                if delivery_note.customer == customer:
                    dn = frappe.get_doc("Delivery Note", delivery_note.delivery_note)
                    if not new_sinv.customer:
                        # populate sales invoice details from first delivery note
                        new_sinv.customer = dn.customer
                        new_sinv.customer_name = dn.customer_name
                        new_sinv.customer_address = dn.customer_address
                        new_sinv.shipping_address_name = dn.shipping_address_name
                        new_sinv.contact_person = dn.contact_person
                        new_sinv.taxes_and_charges = dn.taxes_and_charges
                        new_sinv.currency = dn.currency
                        new_sinv.selling_price_list = dn.selling_price_list
                        new_sinv.items = []
                        new_sinv.sammelrechnung = self.name
                        new_sinv.company = self.company
                        customer_name = dn.customer_name
                    for item in dn.items:
                        new_sinv.append('items', {
                            'item_code': item.item_code,
                            'rate': item.rate,
                            'qty': item.qty,
                            'delivery_note': dn.name,
                            'dn_detail': item.name
                        })
                    # store reference to collected invoice
                    dn.sammelrechnung = self.name
                    dn.save()
            sinv_ref = new_sinv.insert()
            if self.auto_submit:
                sinv_ref.submit()
            frappe.db.commit();
            # add sales invoice reference to collected invoice
            row = self.append('sales_invoices', {
                'sales_invoice': sinv_ref.name, 
                'customer': customer,
                'customer_name': customer_name,
            })
        self.save()
        return
        
    def unlink_docs(self):
        # unlink delivery notes
        for delivery_note in self.delivery_notes:
            dn = frappe.get_doc("Delivery Note", delivery_note.delivery_note)
            dn.sammelrechnung = None
            dn.save()
        # cancel or abort sales invoices
        for sales_invoice in self.sales_invoices:
            sinv = frappe.get_doc("Sales Invoice", sales_invoice.sales_invoice)
            if sinv.docstatus == 1:
                sinv.cancel()
            elif sinv.docstatus == 0:
                sinv.docstatus = 2
                sinv.save()
        return
