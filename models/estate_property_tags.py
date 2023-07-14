from odoo import fields,models

class estatePropertyTags(models.Model):
	_name = "estate.property.tags"
	_description = "it stores tags for properties"
	_order = "name"
	name = fields.Char(required=True)
	color = fields.Integer(string="Color", default= '1')

	#sql constraints
	_sql_constraints = [
        ('check_property_tags', 'unique(name)',
         'Tags must be an unique ')
    ]