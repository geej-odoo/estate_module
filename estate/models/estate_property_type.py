from odoo import models,fields,api

class EstatePropertyType(models.Model):
    _name ="estate.property.type"
    _description="Estate Property Type"
    _log_access=False
    _order = "sequence,name"

    _sql_constraints = [
        ('_unique_name', 'unique (name)',
         " property tag name and property type name must be unique"),
    ]
    

    name=fields.Char(required=True,string="Name")
    sequence = fields.Integer('Sequence', default=1)
    property_ids=fields.One2many('estate.property','property_type_id')


    # #ch12:
    offer_ids=fields.One2many('estate.property.offer','property_type_id',string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count', string="Offer Count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        # print('\n\n\n>>>>>>>>>>>>>>',self)
        # print('self.property_ids >>>>>>>>>>.',self.property_ids)
        for record in self:
            # print('record >>>>>>>>offers',record,record.offer_ids,len(record.offer_ids))
            # offer_count = self.env['estate.property.type'].search_count([('property_type_id', '=', self.propperty_ids)])

            # record.offer_count =record.offer_ids 
            # self.offer_count = 10
            record.offer_count=len(record.offer_ids)
    # @api.depends('offer_ids')
    # def _compute_offer_count(self):
    #     if self.offer_ids:
    #         self.offer_count=self.env['estate.property.offer'].search_count([('property_type_id','=',self.id)])
    #     else:
    #         self.offer_count=0

    
    





    



