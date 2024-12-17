from odoo import models, fields, api
from datetime import timedelta

class BarbershopAppointment(models.Model):
    _name = "barbershop.appointment"
    _description = "Citas"

    name = fields.Char(string="Referencia", required=True)
    start_at = fields.Datetime(string="Desde", required=True)
    end_at = fields.Datetime(string="Hasta", required=False, compute="_compute_end_at", readonly=True)
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    state_id = fields.Many2one('barbershop.state', string="Estado", required=True)
    employee_id = fields.Many2one('hr.employee', string="Empleado", required=True)
    service_ids = fields.Many2many('barbershop.service', string="Servicios", required=True)
    total_price = fields.Float(string="Precio Total", compute="_compute_total_price", store=True, readonly=True)

    @api.depends('service_ids')
    def _compute_total_price(self):
        for appointment in self:
            total = sum(service.price for service in appointment.service_ids)
            appointment.total_price = total

    @api.depends('service_ids')
    def _compute_end_at(self):
        for appointment in self:
            if appointment.start_at:
                total_duration = sum(service.duration for service in appointment.service_ids)
                appointment.end_at = appointment.start_at + timedelta(minutes=total_duration)
            else: 
                appointment.end_at = None   


