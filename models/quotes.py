from odoo import models, fields

class Quotes(models.Model):
    _name = "quotes"
    _description = "citas"

    name = fields.Char(string="Nombre de cliente")
    date = fields.Date(string="Fecha de cita", required=True)
    confirm = fields.Boolean(string="Confirmacion de cita")
    service = fields.Selection([('corte', 'Corte'), ('barba', 'Barba')], string="Servicios")
    user_id = fields.Many2one('customer')