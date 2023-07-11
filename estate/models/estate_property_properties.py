from odoo import models, fields

class EstatePropertyProperties(models.Model):
    _name ="estate.property.properties"
    _description="Estate Property Properties"
    _log_access=False
    _order = "name"

    name=fields.Char(required=True,string="Properties")


    
    



