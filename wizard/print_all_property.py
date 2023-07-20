from odoo import fields,models

class PrintAllPropertyWizard(models.TransientModel):
	_name = "print.all.property.wizard"
	_description = "prints all property"

	old_partner_id = fields.Many2one('res.users', string="Old Partner")
	new_partner_id = fields.Many2one('res.users', string="New Partner")


	def add_info(self):
		print("\n\n\n\n\n\n -----------", self.env.context)
		# property_id = self.env['estate.property'].browse(self.env.context.get('active_id'))

		# property_id = self.env['estate.property'].browse('salesman')
		property_id = self.env['estate.property'].search([('salesman','=',self.old_partner_id.name)])
		print(property_id)
		for rec in property_id:
			# print('>>>>>>>>>',rec.name)
			rec.salesman = self.new_partner_id
			print('successfull...')

	#selling price admin ne dekhavi joia
	#menuitem bas admin ne dekhavi joia
		
