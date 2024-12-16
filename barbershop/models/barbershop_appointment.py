from odoo import models, fields
from odoo.exceptions import ValidationError

class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"

    name = fields.Char(string="Referencia")
    start_at = fields.Datetime(string="Desde", required=True)
    end_at = fields.Datetime(string="Hasta", required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente")
    state_id = fields.Many2one('barbershop.state', string="Estado")
    service_ids = fields.Many2many('barbershop.service', string="Servicios")

    @api.constrains('start_at', 'end_at', 'barber_id')
    def _check_appointment_overlap(self):
        """Evitar conflictos de horarios para el mismo barbero."""
        for record in self:
            overlapping_appointments = self.search([
                ('id', '!=', record.id),
                ('barber_id', '=', record.barber_id.id),
                ('start_at', '<', record.end_at),
                ('end_at', '>', record.start_at),
            ])
            if overlapping_appointments:
                raise ValidationError(
                    "El barbero ya tiene una cita en el rango de horario seleccionado. "
                    "Por favor elija otro horario o barbero."
                )