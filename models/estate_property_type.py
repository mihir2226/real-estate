from odoo import api,fields, models

class estatePropertyType(models.Model):
	_name = "estate.property.type"
	_description = "pecify estate property type"
	_order = "sequence" #manual(sequancing)

	name = fields.Char(required=True)
	property_ids = fields.One2many("estate.property", "property_id")
	sequence = fields.Integer('Sequence', default=1)
	offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
	offer_count = fields.Integer(compute="_compute_offers_count", default=0)

	#sql constraints
	_sql_constraints = [
        ('check_property_type', 'unique(name)',
         'Property type must be an unique ')
    ]
	def find_offer(self):
		offers=self.offer_ids
		print('---->>>>>',offers)
		return {
		'type':'ir.actions.act_window',
		'name':'Offers',
		'view_mode':'tree',
		'res_model':'estate.property.offer',
		'domain': [('id','in',offers.ids)],
		}
	@api.depends("offer_ids")
	def _compute_offers_count(self):
		offers=self.offer_ids
		for id in offers.ids:
			self.offer_count+=1
		
   	#smart button returns action
