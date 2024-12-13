from odoo import http
from odoo.http import request

class BarbershopController(http.Controller):
    @http.route('/barbershop', auth='public', website=True)
    def barbershop_main(self, **kwargs):
        return request.render('barbershop.barbershop_main_view')



    