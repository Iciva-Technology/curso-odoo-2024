from odoo import models, fields, api


class BarbershopService(models.Model):
    _name = "barbershop.service"
    _description = "Servicios"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Html(string="Descripción")
    duration = fields.Integer(string="Duración", help="Duración del servicio expresado en minutos")
    price = fields.Float(string="Precio")
    difficulty = fields.Selection([
        ('easy', 'Fácil'),
        ('medium', 'Medio'),
        ('hard', 'Difícil')], string="Dificultad")
    image = fields.Binary(string="Imagen")
    aftercare = fields.Html(string="Cuidados posteriores")
    appointment_ids = fields.Many2many('barbershop.appointment', string="Citas", required=True, tracking=True)
    task_ids = fields.Many2many('barbershop.task', string="Tareas Relacionadas")
    task_count = fields.Integer(string="Cantidad de tareas", compute="_compute_task_count")

    @api.depends('task_ids')
    def _compute_task_count(self):
        for record in self:
            record.task_count = len(record.task_ids)

    def action_view_tasks(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tareas Relacionadas',
            'view_mode': 'tree,form',
            'res_model': 'barbershop.task',
            'domain': [('id', 'in', self.task_ids.ids)],
            'context': {
                'default_service_id': self.id,
            },
        }
