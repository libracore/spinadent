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
        }
    ]
