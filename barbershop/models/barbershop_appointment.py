from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"

    name = fields.Char(string="Referencia")
    start_at = fields.Datetime(string="Desde", required=True)
    end_at = fields.Datetime(string="Hasta", required=False, compute="_compute_end_at", readonly=True, )
    partner_id = fields.Many2one('res.partner', string="Cliente")
    state_id = fields.Many2one('barbershop.state', string="Estado")
    service_ids = fields.Many2many('barbershop.service', string="Servicios")
    barber_id = fields.Many2one('hr.employee', string="Barbero", required=True)
    total_price = fields.Float(string="Precio Total", compute="_compute_total_price", store=True, readonly=True)

    MAX_APPOINTMENTS_PER_DAY = 3  # Número máximo de citas por barbero al día
    
    @api.depends('service_ids')
    def _compute_total_price(self):
        """Calcula el precio total de los servicios seleccionados."""
        for appointment in self:
            total = sum(service.price for service in appointment.service_ids)
            appointment.total_price = total
            _logger.info(f"Computed total price for appointment {appointment.id}: {total}")
    
    @api.depends('service_ids')
    def _compute_end_at(self):
        """Calcula dinámicamente la hora de finalización en base a la duración total de los servicios."""
        for appointment in self:
            if appointment.start_at:
                # Obtener los registros completos de los servicios
                services = self.env['barbershop.service'].browse(appointment.service_ids.ids)
                total_duration = sum(service.duration for service in services)
                appointment.end_at = appointment.start_at + timedelta(minutes=total_duration)
                _logger.info(f"Computed end_at for appointment {appointment.id}: {appointment.end_at}")
            else:
                appointment.end_at = None
                _logger.warning(f"Missing start_at for appointment {appointment.id}. Cannot compute end_at.")


    def _validate_no_overlap(self, vals):
        """Valida que no existan conflictos de horarios para el barbero."""
        start_at = vals.get('start_at', self.start_at)
        end_at = vals.get('end_at', self.end_at)
        barber_id = vals.get('barber_id', self.barber_id.id)

        _logger.info("Validating appointment overlap...")
        _logger.debug(f"Start: {start_at}, End: {end_at}, Barber: {barber_id}")

        if start_at and end_at and barber_id:
            overlapping_appointments = self.search([
                ('id', '!=', self.id),  # Excluir el registro actual (en caso de edición)
                ('barber_id', '=', barber_id),
                ('start_at', '<', end_at),
                ('end_at', '>', start_at),
            ])
            if overlapping_appointments:
                _logger.warning(f"Overlap detected with appointments: {overlapping_appointments.ids}")
                raise ValidationError(
                    "El barbero ya tiene una cita en el rango de horario seleccionado. "
                    "Por favor elija otro horario o barbero."
                )
        _logger.info("No overlapping appointments found.")

    def _validate_max_appointments_per_day(self, vals):
        """Valida que el barbero no tenga más citas de las permitidas en un día."""
        start_at = vals.get('start_at', self.start_at)
        barber_id = vals.get('barber_id', self.barber_id.id)

        if start_at and barber_id:
            # Obtener la fecha (sin la hora) de la cita
            appointment_date = fields.Date.to_date(start_at)

            # Contar las citas ya programadas para el barbero en esa fecha
            daily_appointments = self.search_count([
                ('barber_id', '=', barber_id),
                ('start_at', '>=', appointment_date),
                ('start_at', '<', fields.Datetime.add(appointment_date, days=1)),
                ('id', '!=', self.id)  # Excluir el registro actual (en caso de edición)
            ])

            _logger.info(f"Barber ID {barber_id} has {daily_appointments} appointments on {appointment_date}.")
            if daily_appointments >= self.MAX_APPOINTMENTS_PER_DAY:
                raise ValidationError(
                    f"El barbero ya tiene el máximo de {self.MAX_APPOINTMENTS_PER_DAY} citas programadas para el día {appointment_date}. "
                    "Por favor elija otra fecha o barbero."
                )

    @api.model
    def create(self, vals):
        """Sobrescribe create para validar conflictos de horarios y número máximo de citas."""
        _logger.info(f"Creating a new appointment with values: {vals}")
        self._validate_no_overlap(vals)
        self._validate_max_appointments_per_day(vals)
        result = super(BarbershopAppointment, self).create(vals)
        _logger.info(f"Appointment created with ID: {result.id}")
        return result

    def write(self, vals):
        """Sobrescribe write para validar conflictos de horarios y número máximo de citas."""
        _logger.info(f"Updating appointment ID(s): {self.ids} with values: {vals}")
        for record in self:
            _logger.debug(f"Validating record with ID: {record.id}")
            record._validate_no_overlap(vals)
            record._validate_max_appointments_per_day(vals)
        result = super(BarbershopAppointment, self).write(vals)
        _logger.info(f"Update completed for appointment ID(s): {self.ids}")
        return result

    def unlink(self):
        for record in self:
            # Archivar la cita en lugar de eliminarla
            record.state_id = self.env.ref('barbershop.state_archived')  # Supón que tienes un estado 'archivado'
            _logger.info(f"Appointment {record.id} archived instead of deleted.")
        return super(BarbershopAppointment, self).unlink()

