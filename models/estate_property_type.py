from odoo import fields, models

class estatePropertyType(models.Model):
	_name = "estate.property.type"
	_description = "pecify estate property type"

	name = fields.Char(required=True)