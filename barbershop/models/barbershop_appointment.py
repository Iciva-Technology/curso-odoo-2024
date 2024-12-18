from odoo import models, fields, api
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

    @api.model
    def create(self, vals):
        record = super(BarbershopAppointment, self).create(vals)
        record.check_appointment_overlap()
        return record

    def write(self, vals):
        res = super(BarbershopAppointment, self).write(vals)
        res.check_appointment_overlap()
        return res

    def check_appointment_overlap(self):
        for rec in self:
            overlapping_appointments = self.env['barbershop.appointment'].search([
                ('partner_id', '=', rec.partner_id.id),
                ('id', '!=', rec.id),  # Excluir la misma cita si es edición
                ('start_at', '<', rec.end_at),
                ('end_at', '>', rec.start_at),
            ])
            if overlapping_appointments:
                raise ValidationError('El cliente ya tiene una cita en el rango de tiempo seleccionado.')


