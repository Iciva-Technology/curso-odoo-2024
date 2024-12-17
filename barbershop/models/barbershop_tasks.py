from odoo import models, fields, api


class BarbershopTasks(models.Model):
    _name = "barbershop.tasks"
    _description = "Tareas"

    name = fields.Char(string="Nombre")
    sequence = fields.Integer(string="Secuencia")
    active = fields.Boolean(string="Activo", default=True)
    description = fields.Html(string='Descripcion')
    state = fields.Selection([
        ('earring', 'Pendiente'),
        ('in progress', 'En proceso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada')], string="Estado",)
    deadline = fields.Date(string="Fecha Limite")
    priority = fields.Selection([
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta')], string="Prioridad")
    realted_service_ids = fields.Many2many('barbershop.service', string="Servicios")
    employee_id = fields.Many2one('hr.employee', string="Empleado")
