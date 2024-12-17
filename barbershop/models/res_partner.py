from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    CI = fields.Char(string="Cedula de Identidad")
    gender = fields.Selection([
        ('female', 'Femenino'),
        ('masculine', 'Masculino'),
        ('other', 'Otro')
    ], string="Genero")