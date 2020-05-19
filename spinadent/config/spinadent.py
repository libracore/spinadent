from __future__ import unicode_literals
from frappe import _

def get_data():
    return[
        {
            "label": _("Sales"),
            "icon": "fa fa-money",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Sammelrechnung",
                       "label": _("Sammelrechnung"),
                       "description": _("Sammelrechnung")
                   }
            ]
        },
        {
            "label": _("Tarpoints Requirements"),
            "icon": "fa fa-money",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Insurance",
                       "label": _("Insurance"),
                       "description": _("Insurance")
                   },
                   {
                       "type": "doctype",
                       "name": "Healthcare Practitioner",
                       "label": _("Healthcare Practitioner"),
                       "description": _("Healthcare Practitioner")
                   }, 
                   {
                       "type": "doctype",
                       "name": "Patient",
                       "label": _("Patient"),
                       "description": _("Patient")
                   }, 
                   {
                       "type": "doctype",
                       "name": "Behandlungsgrund",
                       "label": _("Behandlungsgrund"),
                       "description": _("Behandlungsgrund")
                   }, 
                   {
                       "type": "doctype",
                       "name": "Tarpoint Payment Type",
                       "label": _("Tarpoint Payment Type"),
                       "description": _("Tarpoint Payment Type")
                   }
            ]
        },
         {
            "label": _("Tarpoints export"),
            "icon": "fa fa-money",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Sales Invoice",
                       "label": _("Sales Invoice"),
                       "description": _("Sales Invoice")
                   },
                    {
                       "type": "doctype",
                       "name": "Sales Order",
                       "label": _("Sales Order"),
                       "description": _("Sales Order")
                   },
                    {
                       "type": "doctype",
                       "name": "Quotation",
                       "label": _("Quotation"),
                       "description": _("Quotation")
                   },
                    {
                       "type": "doctype",
                       "name": "Delivery Note",
                       "label": _("Delivery Note"),
                       "description": _("Delivery Note")
                   }
            ]
        }
    ]
