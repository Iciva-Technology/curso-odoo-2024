from odoo import models, fields, api


class BarbershopService(models.Model):
    _name = "barbershop.service"
    _description = "Servicios"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Html(string="Descripción")
    duration = fields.Integer(string="Duración", help="Duración del servicio expresado en minutos")
    number_of_appointments = fields.Integer(string="Número de citas", compute="_compute_number_of_appointments")
    price = fields.Float(string="Precio")
    difficulty = fields.Selection([
        ('easy', 'Fácil'),
        ('medium', 'Medio'),
        ('hard', 'Difícil')], string="Dificultad")
    image = fields.Binary(string="Imagen")
    aftercare = fields.Html(string="Cuidados posteriores")

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
