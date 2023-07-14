from odoo import api,fields,models

class ResUser(models.Model):
	_inherit = "res.users"

	property_ids = fields.One2many('estate.property','salesman',domain=[('state','not in',['sold','cancel'])])
	

	# @api.onchange('property_ids')
	# def onchange_properties(self):
	# 	for rec in self:
	# 		print('>>>>>>>>>>>>>>>>>>>>',rec.property_ids.name)