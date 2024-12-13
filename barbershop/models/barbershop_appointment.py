from odoo import models, fields, api


class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"
    _rec_name = 'partner_id'

    name = fields.Char(string="Referencia")
    partner_id = fields.Many2one('res.partner', string="Cliente")
    start_time = fields.Datetime(string="Desde", required=True)
    end_time = fields.Datetime(string="Hasta", required=True)
    service_ids = fields.Many2many('barbershop.service', string="Servicios")
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
        tracking=True,
        group_expand='_expand_groups'
    )

    @api.model
    def _expand_groups(self, states, domain, order):
        return ['requested', 'confirmed', 'arrived', 'in_service', 'completed', 'cancelled']
    