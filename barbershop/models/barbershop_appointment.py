from odoo import models, fields, api


class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"

    name = fields.Char(string="Referencia", required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True, tracking=True)
    start_time = fields.Datetime(string="Desde", required=True)
    end_time = fields.Datetime(string="Hasta", required=True)
    service_ids = fields.Many2many('barbershop.service', string="Servicios", required=True)
    state = fields.Selection(
        [
            ('requested', 'Solicitado'),
            ('confirmed', 'Confirmado'),
            ('arrived', 'Llegó'),
            ('in_service', 'Siendo atendido'),
            ('completed', 'Finalizado'),
            ('cancelled', 'Cancelado')
        ],
        string="Estado",
        default='requested',
        tracking=True
    )
    confirm = fields.Boolean(string="Confirmacion de cita", default = False)

    def action_confirm(self):
        """Cambia el estado a 'Confirmado'."""
        for record in self:
            record.state = 'confirmed'

    def action_cancel(self):
        """Cambia el estado a 'Cancelado'."""
        for record in self:
            record.state = 'cancelled'
