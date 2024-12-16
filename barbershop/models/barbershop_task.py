from odoo import models, fields


class BarbershopTask(models.Model):
    _name = "barbershop.task"
    _description = "Tareas"

    name = fields.Char(string="Nombre")
    description = fields.Char(string="Descripcion")
    deadline = fields.Date(string="Fecha Limite", required=True)
    employee = fields.Char(string="Empleado")
    priority = fields.Selection([('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta')], string="Prioridad")
    