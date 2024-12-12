from odoo import models, fields


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