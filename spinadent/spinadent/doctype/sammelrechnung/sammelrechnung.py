# -*- coding: utf-8 -*-
# Copyright (c) 2019, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Sammelrechnung(Document):
    def validate(self):
        pass
        
    def before_save(self):
        # run this before saving
        self.collect_values()
 
    def collect_values(self):               
        # get all unpaid sales_invoices
        sql_query = """SELECT `tabSales Invoice`.`name` AS `name`,
        `tabSales Invoice`.`docstatus` AS `doc_status`,
        FROM `tabSales Invoice`
            WHERE 
              `tabSales Invoice`.`docstatus` = 1;"""
        results = frappe.db.sql(sql_query, as_dict=True)

        self.invoices = []
        for result in results:
            row = self.append('invoices', {
                'name': result['name'], 
                'docstatus': result['doc_status']
            })               
               
        return       
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
    #def collect_values(self):
        # get all unpaid sales_invoices
        #sql_query = """SELECT `tabDelivery Note` AS `dlvrnt`,
           #WHERE 
              #`tabSales Invoice`.`docstatus` = 1
              #AND `tabSales Invoice`.`status` = "To Bill" 
              #AND `tabSales Invoice`.`abgeholt` = 0;"""
        #results = frappe.db.sql(sql_query, as_dict=True)
#
        #self.invoices = []
        #for result in results:
            #row = self.append('invoices', {
                #'sales_invoice': result['dlvrnt'], 
            #})
        #
        #return
        
        
