from odoo import api,fields,models,_ ,exceptions
from datetime import date
from datetime import time
from dateutil.relativedelta import relativedelta
from .import estate_property_offer
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name='estate.property'
    _description='Real Estate Firm'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _log_access=False
    _order = "id desc"
    
    _sql_constraints = [
        (
            'check_expected_price', 'CHECK(expected_price>= 0)',
            'expected price must be strictly positive.'
        ),
        (
            'check_selling_price', 'CHECK(selling_price>=0)',
            'selling_price must be positive.'
        ),
    ]

    name = fields.Char(required=True,string='Property')
    description=fields.Text(string='Description')
    postcode=fields.Char(string='Postcode')
    date_availability=fields.Date(copy=False,default=lambda self:fields.Date.today()+ relativedelta(months=3),string='Date Available')
    expected_price=fields.Float(required=True,string='Expected Price')
    selling_price=fields.Float(readonly=True,copy=False, string='Selling Price')
    bedrooms=fields.Integer(default=2, string='Bed Room')
    living_area=fields.Integer(string='Living area(Sqft)')
    facades=fields.Integer(string='Facades')
    garage=fields.Boolean(string='Garage')
    garden=fields.Boolean(string='Garden')
    garden_area=fields.Integer(string='Garden Area')
    color_kanban=fields.Integer(string='color')
    image=fields.Binary(string='Image')
    total_area=fields.Integer(compute='_compute_total',string='Total Area')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')  
    #many2one:
    buyer_id = fields.Many2one("res.users", string="Buyer")
    partner_id =fields.Many2one("res.partner", string="Seller")

    property_type_id = fields.Many2one("estate.property.type")
    #tag_id:many2many
    tag_ids = fields.Many2many("estate.property.tag", string="tags")
    #one2many:
    offer_ids=fields.One2many("estate.property.offer","property_id",string="offers")

    state=fields.Selection(
        selection=[
            ('new','New'),
            ('offer_recieved','Offer Recieved'),
            ('offer_accepted','Offer Accepted'),
            ('solded','Solded'),
            ('cancelled','Cancelled'),
        ],
        string="State",
        default="new",
        required=True, 
        copy=False,
        tracking=True,
        
         
        
    )
    garden_orientation=fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West'),
        ],
        string='Type',

      
    )
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            # print('record >>>>>>>>>.',max(record.offer_ids.mapped('price')))
            record.best_price = max(record.offer_ids.mapped('price'),default=0)  


    @api.depends('living_area','garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area=record.living_area+record.garden_area

    @api.onchange('garden','garden_area')
    def onchange_garden_area(self):
        for record in self:
            if record.garden:
                record.garden_area=10
                record.garden_orientation='north'
            else:
                record.garden_area=0
                record.garden_orientation=''         
    
     #ch 10:
    # @api.depends('state')
    def solded(self):
        for record in self:
            if(record.state =='cancelled'):
                raise UserError(_('cancelled property cannot be sold'))
            record.state='solded' 

    def cancelled(self):
        for record in self:
            if (record.state=='solded'):
                raise UserError(_('solded property cannot be cancel'))             
            record.state='cancelled'  

    def unlink(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise exceptions.ValidationError("only new and cancelled properties can be deleted")


    def make_offer(self):
        return {
            'name': ('Real Estate Wizard'),
            'type': 'ir.actions.act_window',
            'res_model': 'estate.wizard',
            'view_mode': 'form',
            'target': 'new'
      }



    
        






