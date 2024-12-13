from odoo import models, fields, api


class BarbershopTask(models.Model):
    _name = "barbershop.task"
    _description = "Tareas"

    name = fields.Char(string="Nombre de la tarea", required=True)
    description = fields.Html(string="Descripción")
    state_task = fields.Selection([
        ('pending', 'Pendiente'),
        ('in_progress', 'En proceso'),
        ('completed', 'Completada'),
        ('cancelled','Cancelada')], 
        string="Estado de la tarea",
        group_expand = '_expand_groups')
    limit_date = fields.Datetime(string="Fecha límite")
    priority_task = fields.Selection([
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high','Alta')], string="Prioridad de la tarea")
    employee_id = fields.Many2one('res.users', string="Empleado encargado")
    service_ids = fields.Many2many('barbershop.service', string="Servicios relacionados")

    @api.model
    def _expand_groups(self, states, domain, order):
        return ['pending', 'in_progress', 'completed', 'cancelled']
    