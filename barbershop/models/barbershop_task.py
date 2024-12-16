from odoo import models, fields


class BarbershopTask(models.Model):
    _name = "barbershop.task"
    _description = "Tareas"

    name = fields.Char(string="Nombre")
    description = fields.Char(string="Descripcion")
    deadline = fields.Date(string="Fecha Limite", required=True)
    employee_id = fields.Many2one('hr.employee', string="Empleado")
    priority = fields.Selection([('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta')], string="Prioridad")
    state = fields.Selection([
        ('assigned', 'Asignada'),
        ('process', 'En Proceso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada')], string="Estado")
