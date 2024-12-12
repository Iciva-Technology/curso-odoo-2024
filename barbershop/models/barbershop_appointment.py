from odoo import models, fields


class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"

    name = fields.Char(string="Referencia")
    date = fields.Date(string="Fecha de cita", required=True)
    confirm = fields.Boolean(string="Confirmacion de cita")
    partner_id = fields.Many2one('res.partner', string="Cliente")
    service_ids = fields.Many2many('barbershop.service', string="Servicios")
