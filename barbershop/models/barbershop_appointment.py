from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"

    name = fields.Char(string="Referencia")
    active = fields.Boolean(string='Activo', default=True)
    start_at = fields.Datetime(string="Desde", required=True)
    end_at = fields.Datetime(string="Hasta", required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente")
    state_id = fields.Many2one('barbershop.state', string="Estado")
    service_ids = fields.Many2many('barbershop.service', string="Servicios")

    def write(self, vals):
        if not vals.get('active', True):
            vals['state_id'] = self.env.ref('barbershop.barbershop_state_cancelled').id
        return super(BarbershopAppointment, self).write(vals)
