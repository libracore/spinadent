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
        sql_query = """SELECT `tabSales Invoice` AS `sinv`,
            FROM `tabSales Invoice`
            WHERE 
                `tabSales Invoice`.`docstatus` = 1;
        """
        results = frappe.db.sql(sql_query, as_dict=True)
        
        self.invoices = []
        for result in results:
            row = self.append('invoices', {
                'sales_invoice': result['sinv'], 
            })
