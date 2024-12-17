from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    barber_id = fields.Many2one('barbershop.appointments', string="Barbero")
    amount_appointments = fields.Integer(string="Cantidad de Citas", compute="_compute_amount_appointments")
    active = fields.Boolean(string="Activo", default=True)

    @api.depends('barber_id')
    def _compute_amount_appointments(self):
        for rec in self:
            rec.amount_appointments = len(rec.barber_id)

    def barber_appointment_id(self):
        self.ensure_one()
        active_id = self.env.context.get('barber_id')
        action = self.env["ir.actions.actions"]._for_xml_id("barbershop.barbershop_appointment_action")
        action['domain'] = [('service_ids', '=', active_id)]
        return action