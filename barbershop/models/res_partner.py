from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    id_number = fields.Char(string="Cedula de Identidad", required=True)
    gender = fields.Selection([
        ('female', 'Femenino'),
        ('masculine', 'Masculino'),
        ('other', 'Otro')
    ], string="Genero", required=True)