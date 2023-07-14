note : ignore all <code></code> tags inside documentation.


#odoo Documentation

<!-- chapter 1 Intro-->
-> The architechure of odoo is consist of 3 layers

	1. Presentation [HTML, CSS, JS]
	2. Logic [Python]
	3. Data [Postgres]

-> Module Structure

	module (estate)
	|
	--models (estate_property, estate.offers)
	|	|_ *.py
	|	|_ __init__.py
	|
	|_view
	|	|_*.xml (estate_property_view)
	|
	|_security
	|	|_ir.model.access.csv
	|
	|_ __init__.py
	|_ __manifest__.py

<!-- chapter 2 Module-->


-> file layout of module.

[module.__init__.py]
<code>from . import models</code>


[module.__manifest__.py]
<code>
	{
		'name':'real estate', <!-- this name show on module (required)-->
		'summary':'this shows what your module does',
		'version':'1.0', <!-- (required) -->
		'category':'sales',
		'website': 'url',
    	'author': 'Mihir nayak', <!-- (required) -->
		'depends':[on which modules it depends],<!-- (required) -->
		'data':[
			'security/ir.model.accesss.csv',
			'view/estate_property_view.xml',
		] <!-- (required) -->
	}
</code>


[module.models.__init__.py]
<code> from . import model_name </code>


[module.models.model_name.py]
<code>
	from odoo import field, models

	class ModelName(models.Model):
		_name="model.name"
		_description="model description"

		name = fields.Char() <!-- field creation -->
</code>


<!-- chapter 3 Basics of fields-->

-> Types of fields:
	1. Text
	2. Char
	3. Integer
	4. Float
	5. Boolean
	6. Date
	7. Selection

	ex:
	name = fields.Char()
	age = fields.Integer()

-> Attributes of fields:
	1. string : for label of thee field in ui
	2. required : if True we have to must insert data in that field. default False
	3. help : Provide long-form help tooltip for users in ui

-> Automatic Fields: fields created by odoo automatically
	1. id
	2. create_time
	3. create_uid
	4. write_time
	5. write_uid


<!-- chapter 4 Security bascs-->

-> data file(csv):
	ir.model.access.csv

-> Access rights: 
	-> When no access rights are defined on a model, Odoo determines that no users can access the data. It is even notified in the log:

	ex:
	WARNING rd-demo odoo.modules.loading: The models ['estate.property'] have no access rules in module estate, consider adding some, like:
	id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink

	-> Access rights are defined as records of the model ir.model.access.

	ex:
	id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
	access_test_model,access_test_model,model_test_model,base.group_user,1,0,0,0


<!-- chapter 5 Play with ui -->

-> There are lot of views in odoo
	1. tree
	2. form
	3. search
	4. kanban
	5. graph
	6. activity
	etc..


->lets create tree view:
	-> first create view for your model.
		ex: estate_property_view.xml 

	[views.estate_property_view.xml]:
	<code>
		<?xml version="1.0" encoding="utf-8"?>
		<odoo>
			<record id="estate_property_tree" model="ir.ui.view">
				<field name="name">estate.property.tree</field>
				<field name="model">estate.property</field>
				<field name="arch" type="xml">
					<tree>
						<field name="name"/> <!-- fields difined in model -->
					</tree>
				</field>
			</record>
		</odoo>
	</code>


-> now we have to create an action for our model.
	<code>
		<record id="estate_property_action" model="ir.ui.actions.act_window">
			<field name="name">Estate</field>
			<field name="res_model">estate.property</field>
			<field name="view_mode">tree</field>
		</record>
	</code>


-> lets create menu for our action
	<code>
		<menuitem 
		id="estate_property_menu" 
		action="estate_property_action" name="Real estate"/>
	</code>

-> Wait a little, we are going to make it little more fun. lets create tabs for our module.
	<code>
		<menuitem 
		id="estate_property_menu_root" 
		action="estate_property_action" name="Real estate"/>
			<menuitem
			id="advertise_menu"
			name="Advertising" parent="estate_property_menu_root"/>
		<menuitem 
		id="estate_property_menu" 
		name="Properties"
		parent="advertise_menu" action="estate_property_action"/>
	</code>


-> so as we created tree view, now we are going to create another view named form view.
	<code>
		<record id="estate_property_form" model="ir.ui.form">
			<field name="name">estate.property.form</field>
			<field name="model">estate.property</field>
			<field name="arch" type="xml">
				<form>
					<sheet>
						<field name="name"/>
						<field name="age"/>
						<field name="dob"/>
					</sheet>
				</form>
			</field>
		</record>
	</code>

-> we can add pages inside form view: so lets see how to do that.
	<code>
		<notebook>
            <page string="Description">
                <field name="description"/>
            </page>
        </notebook>
	</code>

-> until now we seen how to create tree view and form view. but what if we want to search something from search bar. so for that purpose we have to create search view.
	<code>
		<record id="estate_property_search" model="ir.ui.view">
			<field name="name">estate.property.search</field>
			<field name="model">estate.property</field>
			<field name="arch" type="xml">
				<search>
					<field name="name"/>
					<field name="age"/>
					<field name="dob"/>
					<field name="gender"/>
				</search>
			</field>
		</record>	
	</code> 

-> now lets create filters in search view:
	<code>
		<filter string="Available" name="available" domain="[('age','>','18')]"/>
	</code>
	-> it adds filter to our model

-> now lets create group functionality for our model.
	<code>
		<group expan="1" string="Group By">
			<filter string="Gender" name="gender" context="{'group_by':'gender'}"/>
			<filter string="Age" name="age" context="{'group_by':'age'}"/>
		</group>
	</code>


<!-- chapter 7 Relation betweens models -->
-> Now after learning some ui fun stuffs. lets learn how two or more models share data across.

-> there are 3 types of relation we can establish between models:
	1. Many2one
	2. Many2many
	3. One2many

Many2one:
	-> Many2one field you can select only one value from related module.

	ex:
	<code>
		#estate property model
		from odoo import fields, models

		class EstateProperty(models.Model):
			_name = 'estate.property'
			_description = "its estate main table"

			property_type_id = fields.Many2one('estate.property.type' string="Property Type")
	</code>

	-> estate_property_type model.
	
	<code>
		from odoo import fields, models

		class EstatePropertyType(models.Model):
			_name = 'estate.property.type'
			_description = "this table contain types of properties"

			name = fields.Char()
	</code>


Many2many:
	-> Many2many field you can select multiple value from related module.

	ex:
	<code>
		#estate property model
		from odoo import fields, models

		class EstateProperty(models.Model):
			_name = 'estate.property'
			_description = "its estate main table"

			property_tags_ids = fields.Many2many('estate.property.tags' string="Property Tags")
	</code>

	-> estate_property_tags model.

	<code>
		from odoo import fields, models

		class EstatePropertyTags(models.Model):
			_name = 'estate.property.tags'
			_description = "this table contain tags of properties"

			name = fields.Char()
	</code>

One2many:
	-> One2many field you can create new records(values) from related module.

	ex:
	<code>
		#estate property model
		from odoo import fields, models

		class EstateProperty(models.Model):
			_name = 'estate.property'
			_description = "its estate main table"

			property_offers_ids = fields.One2many('estate.property.offers', '' )
	</code>

	-> estate_property_offers model.
	-> Whenever you using One2many do not forget to add inverse Many2one key in the model you relating.

	<code>
		from odoo import fields, models

		class EstatePropertyOffers(models.Model):
			_name = 'estate.property.offers'
			_description = "this table contain offers for properties"

			price = fields.Float()
			state = fields.Selection(selection=[('accept','Accepted'),('reject','Refused')],copy=False)
			partner_id = fields.Many2one("res.partner", required=True) 
			property_id = fields.Many2one("estate.property", required=True) 
			validity = fields.Integer(default = 7)
			deadline = fields.Date()
	</code>

	-> estate_property_offers_view view.

	<code>
		<?xml version="1.0" encoding="UTF-8"?>
		<odoo>
			<record id="estate_offer_tree" model="ir.ui.view">
		        <field name="name">estate.offer.tree</field>
		        <field name="model">estate.property.offer</field>
		        <field name="arch" type="xml">
		            <tree string="Property offer" editable="bottom">
		               <field name="price"/>
		               <field name="partner_id"/>
		               <field name="state"/>
		               <field name="validity" string="Validity(days)"/>
		               <field name="deadline"/>
		            </tree>
		        </field>
		    </record>

			<record id="estate_offer_form" model="ir.ui.view">
				<field name="name">estate.offer.form</field>
		        <field name="model">estate.property.offer</field>
		        <field name="arch" type="xml">
		        	<form string="Offers">
		        		<sheet>
		                    <group>
		                        <field name="price"/>
		                        <field name="partner_id"/>
		                        <field name="property_id"/>
		                        <field name="validity" string="Validity(days)"/>
		                        <field name="deadline"/>
		                        <field name="state"/>
		                    </group>
		        		</sheet>
		        	</form>
		        </field>
			</record>
		</odoo>
	</code>

	-> Now create view for One2many field inside estate_property_view (form view)

	<code>
		<?xml version="1.0" encoding="UTF-8"?>
		<odoo>
			<notebook>
				<page string="Offers">
	                <field name="offer_ids">
	                    <tree string='offer'>
	                        <field name='price' string='Price'/>
	                        <field name='partner_id' string='Partner'/>
	                        <field name="validity" string="Validity(days)"/>
	                        <field name="deadline"/>
	                        <field name='state'/>
	                    </tree>
	                </field>
	            </page>
	        </notebook>
		</odoo>
	</code>


	#Note
	-> The object self.env gives access to request parameters and other useful things:

		-> self.env.cr or self._cr is the database cursor object; it is used for querying the database

		-> self.env.uid or self._uid is the current user’s database id

		-> self.env.user is the current user’s record

		-> self.env.context or self._context is the context dictionary

		-> self.env.ref(xml_id) returns the record corresponding to an XML id

		-> self.env[model_name] returns an instance of the given model


<!-- chapter 8 Compute fields and Onchanges -->
	-> Untill now we leaned about relational fields, models, views and fields. so today we are going to learn new type of fields:
		
		1. Computed_fields
		2. Onchanges







<!-- Build report -->
	->




	





