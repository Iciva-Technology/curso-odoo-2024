from odoo import models, fields, api


class BarbershopService(models.Model):
    _name = "barbershop.service"
    _description = "Servicios"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Html(string="Descripción")
    duration = fields.Integer(string="Duración", help="Duración del servicio expresado en minutos")
    number_of_appointments = fields.Integer(string="Número de citas", compute="_compute_number_of_appointments")
    number_of_tasks = fields.Integer(string="Número de tareas", compute="_compute_number_of_tasks")
    counts_appoinments_ids = fields.Many2many('barbershop.appointments', string="Citas")
    counts_tasks_ids = fields.Many2many('barbershop.tasks', string="Tareas")
    price = fields.Float(string="Precio")
    difficulty = fields.Selection([
        ('easy', 'Fácil'),
        ('medium', 'Medio'),
        ('hard', 'Difícil')], string="Dificultad")
    image = fields.Binary(string="Imagen")
    aftercare = fields.Html(string="Cuidados posteriores")

    @api.depends('counts_appoinments_ids')
    def _compute_number_of_appointments(self):
        for rec in self:
            appointment_ids = self.env['barbershop.appointment'].search([('service_ids', 'in', rec.id)])
            rec.number_of_appointments = len(appointment_ids)

    def action_appointment_id(self):
        self.ensure_one()
        active_id = self.env.context.get('active_id')
        action = self.env["ir.actions.actions"]._for_xml_id("barbershop.barbershop_appointment_action")
        action['domain'] = [('service_ids', '=', active_id)]
        return action
    
    @api.depends('counts_tasks_ids')
    def _compute_number_of_tasks(self):
        for rec in self:
            tasks_ids = self.env['barbershop.tasks'].search([('realted_service_ids', 'in', rec.id)])
            rec.number_of_tasks = len(tasks_ids)

    def action_tasks_id(self):
        self.ensure_one()
        tasks_active_id = self.env.context.get('tasks_active_id')
        tasks_action = self.env["ir.actions.actions"]._for_xml_id("barbershop.action_barbershop_tasks")
        tasks_action['domain'] = [('realted_service_ids', '=', tasks_active_id)]
        return tasks_action