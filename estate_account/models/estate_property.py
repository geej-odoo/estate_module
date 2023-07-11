from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"
    _description = "estate property account"



    def solded(self):
            self.env['account.move'].create({
            'partner_id': self.partner_id.id,
                'move_type': 'out_invoice', 
                "line_ids": [
                    Command.create({
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06
                    }),
                    Command.create({
                        'name':self.name,
                        'quantity': 1,
                        'price_unit': 100
                    })   
                ],

            })

            return super().solded()


    # <record id="product_uom_dozen" model="uom.uom">
    #     <field name="category_id" ref="uom.product_uom_categ_unit"/>
    #     <field name="name">Dozens</field>
    #     <field name="factor_inv" eval="12"/>
    #     <field name="uom_type">bigger</field>
    # </record>



    






    
   
