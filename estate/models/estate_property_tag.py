from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name ="estate.property.tag"
    _description="Estate Property Tag"
    _log_access=False
    _order = "name"

    name=fields.Char(required=True,string="Property Tags")
    color=fields.Integer()

    
    



