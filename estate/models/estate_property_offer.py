from odoo import api, models, fields, exceptions
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError, UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price>=0)',
         'Offer Price Must Be Positive')
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ], copy=False , string="Status")
    partner_id = fields.Many2one("res.partner", required=True ,string="Partner")
    property_id = fields.Many2one("estate.property", required=True,string="Property")
    property_type_id = fields.Many2one(related="property_id.property_type_id",string="Property Type")
    # ch9
    validity = fields.Integer(string="Validity(In days)")
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_compute_inverse_date_deadline')

    @api.model
    def create(self, vals):
        temp = self.env['estate.property'].browse(vals['property_id'])
        if vals['price'] < temp.best_price:
            raise ValidationError(
                'Offer must be highr than %.2f' % temp.best_price)
        else:
            temp.state = 'offer_recieved'
            return super().create(vals)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + \
                    relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + \
                    relativedelta(days=record.validity)

    def _compute_inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline -
                               record.create_date.date()).days

    # ch10

    def offer_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            record.property_id.state = 'offer_accepted'
            # record.write({'status':'accepted',
            # record.property_id.selling_price=record.price
            # record.property_id.partner_id=record.partner_id
            # })

    def offer_rejected(self):
        for record in self:
            record.status = "refused"




    




    # @api.constrains('selling_price', 'expected_price')
    # def _check_selling_price(self):
    #     for record in self:
    #         if (
    #             not float_is_zero(record.selling_price, precision_digits=2)
    #             and not float_is_zero(record.expected_price, precision_digits=2)
    #             and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1
    #         ):
    #             raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    # @api.model
    # def create(self, vals):
    #     if vals.get('property_id'):
    #         property_id = self.env['estate.property'].browse(
    #             vals['property_id'])
    #         existing_offer = self.search(
    #             [('property_id', '=', vals['property_id'])], order='price desc', limit=1)
    #         if existing_offer and vals.get('price') and vals['price'] < existing_offer.price:
    #             raise exceptions.ValidationError(
    #                 "the price should be greater than the existing price", existing_offer)
    #         property_id.write({'state': 'offer_recieved'})
    #     return super(EstatePropertyOffer, self).create(vals)
