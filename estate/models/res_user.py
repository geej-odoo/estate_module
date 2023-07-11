from odoo import fields, models

class ResUser(models.Model):
    _inherit = "res.users"
    
    property_ids=fields.One2many('estate.property','buyer_id',string="Property ID",domain="['|',('state','=','new'),('state','=','offer_recieved')]")

    
