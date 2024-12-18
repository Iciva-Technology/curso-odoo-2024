from odoo import models, fields, api


class BarbershopTask(models.Model):
    _name = "barbershop.task"
    _description = "Tareas"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Html(string="Descripción")
    state = fields.Selection(
        selection=[
            ('to_do', 'Pendiente'),
            ('in_process', 'En Proceso'),
            ('done', 'Completada'),
            ('cancel', 'Cancelada'),
        ],
        string='Estado',
        default='to_do',
        group_expand='_group_expand_states'

    )
    end_at = fields.Datetime(string="Fecha limite", required=True)
    priority = fields.Selection(
        selection=[
            ('low', 'Baja'),
            ('middle', 'Media'),
            ('high', 'Alta'),
        ],
        string='Prioridad'
    )
    

    employee_id = fields.Many2one(
        'hr.employee',       
        string='Empleado',  
        help='Selecciona un empleado',
    )
    service_ids = fields.Many2many('barbershop.service', string="Servicios")



    def _group_expand_states(self, states, domain, order):
        return [key for key, val in self._fields['state'].selection]

