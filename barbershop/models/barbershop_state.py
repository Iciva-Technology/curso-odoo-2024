from odoo import models, fields


class BarbershopState(models.Model):
    _name = "barbershop.state"
    _description = "Estados"

    name = fields.Char(string="Nombre", required=True)
    sequence = fields.Integer(string="Secuencia")
    active = fields.Boolean(string="Activo", default=True)
