from odoo import models, fields


class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"

    name = fields.Char(string="Referencia")
    start_at = fields.Datetime(string="Desde", required=True)
    end_at = fields.Datetime(string="Hasta", required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente")
    state_id = fields.Many2one('barbershop.state', string="Estado")
    service_ids = fields.Many2many('barbershop.service', string="Servicios")
