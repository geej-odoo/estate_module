from odoo import models, fields


class EsateWizard(models.TransientModel):
    _name = 'estate.wizard'
    _description = 'Estate Wizard '
    
    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),

        ],
        copy=False
    )
    partner_id =fields.Many2one("res.partner", string="Seller")

    def create_wizard(self):
        selected_property=self.env.context.get('active_ids')
        for record in selected_property:
            self.env['estate.property.offer'].create(
                {
                    'price':self.price,
                    'partner_id':self.partner_id.id,
                    'property_id':record

                }
            )
        return True



    
