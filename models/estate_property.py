from odoo import api,fields, models
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property" #it converts . into _ and create table of that name
    _description = "estate property details"

    name = fields.Char(string="Title",required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", default=lambda self:date.today()+relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(default="2")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('n','North'),('s','South'),('e','East'),('w','West')]) 
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new','New'),('accept','Offer Accepted'),('reject','Offer Rejected'),('sold','Sold'),('cancel','Canceled')],string="Status", default="new", copy=False) 
    salesman = fields.Many2one('res.partner')
    buyer = fields.Many2one('res.partner')
    
    # relation between tables
    property_id = fields.Many2one("estate.property.type", string="Property Type")
    tags_ids = fields.Many2many("estate.property.tags", "rel_property_tag", "property_id", "tag_id", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    #computed fields and Onchanges
    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(compute="_best_price")

    @api.depends("living_area","garden_area")
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
            