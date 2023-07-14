from odoo import api,fields, models,_
from datetime import date,timedelta
from odoo.exceptions import UserError

class estatePropertyOffer(models.Model):
	_name = "estate.property.offer"
	_description = "it store offer state details"
	_order = "price desc"

	price = fields.Float()
	state = fields.Selection(selection=[('accept','Accepted'),('reject','Refused')],copy=False)
	partner_id = fields.Many2one("res.partner", required=True) 
	property_id = fields.Many2one("estate.property", required=True) 
	validity = fields.Integer(default = 7)
	deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')
	property_type_id = fields.Many2one(related='property_id.property_id', store=True)

	@api.model
	def create(self, vals):
		property = self.env['estate.property'].browse(vals['property_id'])
		if vals['price'] < property.best_price:
			raise UserError(_('Cannot create offer with a lower amount than $%d',property.best_price))
		property.state = 'recieved'
		return super().create(vals)

	@api.depends("validity")
	def _compute_deadline(self):
		for record in self:
			record.deadline = False
			if record.validity:
				record.deadline = date.today()+timedelta(days=record.validity)

	def _inverse_deadline(self):
		for record in self:
			if record.deadline:
				record.validity = (record.deadline - date.today()).days


	def accept_button(self):
		for rcs in self:
			if rcs.property_id.state != "accept" and rcs.property_id.state != "sold" and rcs.property_id.state != "cancel":
				rcs.state = "accept"
				for prcs in rcs.property_id:
					prcs.state = "accept"
					prcs.selling_price = rcs.price
					prcs.buyer = rcs.partner_id
			else:
				raise UserError(_("Offer is accepted for %s property" % rcs.property_id.name))
			
	def reject_button(self):
		for rcs in self:
			if rcs.property_id.state != "sold" or rcs.property_id.state != "cancel":
				rcs.state = "reject"
				# rcs.property_id.state="reject"
				rcs.property_id.selling_price = ''
				rcs.property_id.buyer = ''

	#sql constraints
	_sql_constraints = [
        ('check_offer_price', 'CHECK(price >= 0)',
         'Offer price must be a positive')
    ]