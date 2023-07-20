from odoo import api, fields, models, _
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"  # it converts . into _ and create table of that name
    _description = "estate property details"
    _order = "id desc"  # model(sequancin)

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From", default=lambda self: date.today()+relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(default="2")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('n', 'North'), ('s', 'South'), ('e', 'East'), ('w', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new', 'New'), ('recieved', 'Offer Recieved'), ('accept', 'Offer Accepted'), (
        'reject', 'Offer Rejected'), ('sold', 'Sold'), ('cancel', 'Canceled')], default="new", copy=False)
    salesman = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner')

    # relation between tables
    property_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    tags_ids = fields.Many2many(
        "estate.property.tags", "rel_property_tag", "property_id", "tag_id", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    # computed fields and Onchanges
    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(compute="_best_price")
    

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends("offer_ids")
    def _best_price(self):
        for rec in self:
             rec.best_price = max(rec.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden == False:
            self.garden_orientation = ""
            self.garden_area = ""
        else:
            self.garden_area = 10
            self.garden_orientation = "n"


    @api.onchange("offer_ids")
    def onchange_state(self):
        for rec in self:
            if len(rec.offer_ids) > 0:
                rec.state = "recieved"
            else:
                rec.state = "new"

    # sold button

    def sold_button(self):  #
        for rec in self:
            for orec in rec.offer_ids:
                if rec.state != "cancel":
                    if rec.state == "accept":
                        rec.state = "sold"
                    elif rec.state != 'accept' and rec.state != 'sold':
                        raise UserError(_("you didn't accepted any offer"))    
                else:
                    raise UserError(_("Sold Property Can Not Be Cancled"))
                    #'_' is used for translation


    def cancel_button(self):
        for rec in self:
            if rec.state != "sold":
                rec.state = "cancel"
            else:
                raise UserError(_("Canceled Property Can Not Be Sold"))
                
    # sql constarints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',
         'Expected price must be a positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'Selling price must be a positive')
    ]

    # python constraints
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for rcs in self:
            for prcs in rcs.offer_ids:
                if prcs.state != 'accept' and rcs.selling_price != 0:
                    if rcs.selling_price < (rcs.expected_price*90)/100:
                        raise UserError(_('Selling price must be 90% of expected price or more'))


    def unlink(self):
        for rec in self:
            if rec.state == 'new' or rec.state == 'cancel':
                return super().unlink()
            else:
                raise UserError('You can not delete unless its new or cancled property.')

    #wizard
    # def add_info(self):
    #     offers=self.offer_ids
    #     print('---->>>>>',offers)
    #     return {
    #     'type':'ir.actions.act_window',
    #     'name':'Print All Property',
    #     'view_mode':'form',
    #     'res_model':'print.all.property.wizard',
    #     'domain': [('id','in',offers.ids)],
    #     }

