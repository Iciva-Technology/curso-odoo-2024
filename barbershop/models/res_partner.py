from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    appointment_ids = fields.One2many('barbershop.appointment', 'partner_id', string='Citas')

