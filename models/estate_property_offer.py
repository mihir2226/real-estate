from odoo import api,fields, models
from datetime import date,timedelta


class estatePropertyOffer(models.Model):
	_name = "estate.property.offer"
	_description = "it store offer state details"

	price = fields.Float()
	state = fields.Selection(selection=[('accept','Accepted'),('reject','Refused')], copy=False)
	partner_id = fields.Many2one("res.partner", required=True) 
	property_id = fields.Many2one("estate.property", required=True) 
	validity = fields.Integer(default = 7)
	deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

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
			