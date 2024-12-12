from odoo import models, fields

class Customer(models.Model):
    _name = "customer"
    _description = "Cliente"

    name = fields.Char(string="Nombre")
    last_name = fields.Char(string="Apellido")
    phone = fields.Char(string="Telefono")
    age = fields.Integer(string="Edad")
    email = fields.Char(string="Email")
    gender = fields.Selection(selection=[('male', 'Masculino'), ('fale', 'Femenino')], string="Genero")
    date = fields.Date(string="Fecha de nacimiento")
    quotes_ids = fields.One2many('barbershop.appointment', 'user_id')
