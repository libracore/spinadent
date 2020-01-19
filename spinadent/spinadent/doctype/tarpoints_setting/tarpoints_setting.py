# -*- coding: utf-8 -*-
# Copyright (c) 2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class TarPointsSetting(Document):
    # prepare transfer file
    def render_transfer_file(self):
        data = {
            'transactions': self.get_individual_transactions(restrict_currencies)
        }            
            
        # change path to template
        content = frappe.render_template('erpnextswiss/erpnextswiss/doctype/tarpoints_setting/transfer_file.html', data)
        return {'content': content}
