from odoo import fields,models

class estatePropertyTags(models.Model):
	_name = "estate.property.tags"
	_description = "it stores tags for properties"

	name = fields.Char(required=True)