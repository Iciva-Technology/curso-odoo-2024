from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta

class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"

    name = fields.Char(string="Referencia")
    start_at = fields.Datetime(string="Desde", required=True)
    end_at = fields.Datetime(string="Hasta")
    partner_id = fields.Many2one('res.partner', string="Cliente")
    state_id = fields.Many2one('barbershop.state', string="Estado")
    service_ids = fields.Many2many('barbershop.service', string="Servicios")
    amount_services = fields.Float(string="Monto de servicios", compute="_compute_amount_services")
    barber_id = fields.Many2one('hr.employee', string="Barbero")

    @api.depends('service_ids')
    def _compute_amount_services(self):
        for rec in self:
            for item in rec.service_ids:
                rec.amount_services += item.price

    def prueba(self):
        for rec in self:
            total = 0
            for item in rec.service_ids:
                total += item.price
                _logger.info(f'\n\n\n\n\n {total} \n\n\n\n\n\n')