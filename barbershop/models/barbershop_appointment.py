from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"

    name = fields.Char(string="Referencia")
    start_at = fields.Datetime(string="Desde", required=True)
    end_at = fields.Datetime(string="Hasta", compute="_compute_end_at", store=True)
    partner_id = fields.Many2one('res.partner', string="Cliente")
    state_id = fields.Many2one('barbershop.state', string="Estado")
    service_ids = fields.Many2many('barbershop.service', string="Servicios")
    amount_services = fields.Float(string="Monto de servicios", compute="_compute_amount_services", store=True)
    barber_id = fields.Many2one('hr.employee', string="Barbero")
    max_appointments = 5

    @api.depends('service_ids')
    def _compute_amount_services(self):
        for rec in self:
            rec.amount_services = sum(service.price for service in rec.service_ids)

    @api.depends('start_at', 'service_ids')
    def _compute_end_at(self):
        for appointment in self:
            if appointment.start_at:
                services = self.env['barbershop.service'].browse(appointment.service_ids.ids)
                total_duration = sum(service.duration for service in services)
                appointment.end_at = appointment.start_at + timedelta(minutes=total_duration)
    
    def _validate_no_overlap(self, vals):
        start_at = vals.get('start_at', self.start_at)
        end_at = vals.get('end_at', self.end_at)
        barber_id = vals.get('barber_id', self.barber_id.id)

        _logger.info("Validating appointment overlap...")
        _logger.debug(f"Start: {start_at}, End: {end_at}, Barber: {barber_id}")

        if start_at and end_at and barber_id:
            overlapping_appointments = self.search([
                ('id', '!=', self.id),
                ('barber_id', '=', barber_id),
                ('start_at', '<', end_at),
                ('end_at', '>', start_at),
            ])
            if overlapping_appointments:
                _logger.warning(f"Overlap detected with appointments: {overlapping_appointments.ids}")
                raise ValidationError(
                    "El barbero ya se encuentra ocupado en esa hora. "
                    "Escoja otro horario o barbero."
                )
        _logger.info("No overlapping appointments found.")

    def _validate_max_appointments_per_day(self, vals):
        start_at = vals.get('start_at', self.start_at)
        barber_id = vals.get('barber_id', self.barber_id.id)

        if start_at and barber_id:
            appointment_date = fields.Date.to_date(start_at)

            daily_appointments = self.search_count([
                ('barber_id', '=', barber_id),
                ('start_at', '>=', appointment_date),
                ('start_at', '<', fields.Datetime.add(appointment_date, days=1)),
                ('id', '!=', self.id)
            ])

            _logger.info(f"Barber ID {barber_id} has {daily_appointments} appointments on {appointment_date}.")
            if daily_appointments >= self.MAX_APPOINTMENTS_PER_DAY:
                raise ValidationError(
                    f"El barbero ya tiene el máximo de {self.MAX_APPOINTMENTS_PER_DAY} citas programadas para el día {appointment_date}. "
                    "Por favor elija otra fecha o barbero."
                )

    @api.model
    def create(self, vals):
        _logger.info(f"Creating a new appointment with values: {vals}")
        self._validate_no_overlap(vals)
        self._validate_max_appointments_per_day(vals)
        result = super(BarbershopAppointment, self).create(vals)
        _logger.info(f"Appointment created with ID: {result.id}")
        return result

    def write(self, vals):
        _logger.info(f"Updating appointment ID(s): {self.ids} with values: {vals}")
        for record in self:
            _logger.debug(f"Validating record with ID: {record.id}")
            record._validate_no_overlap(vals)
            record._validate_max_appointments_per_day(vals)
        result = super(BarbershopAppointment, self).write(vals)
        _logger.info(f"Update completed for appointment ID(s): {self.ids}")
        return result
    
    def prueba(self):
        for rec in self:
            total = 0
            for item in rec.service_ids:
                total += item.price
                _logger.info(f'\n\n\n\n\n {total} \n\n\n\n\n\n')