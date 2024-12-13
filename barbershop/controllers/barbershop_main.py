from odoo import http
from odoo.http import request

class BarbershopMain(http.Controller):
    @http.route('/barbershop/main', type='http', auth='user')
    def main_view(self):
        return request.render('barbershop.barbershop_main_view', {})