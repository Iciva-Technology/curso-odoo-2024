from odoo import http
from odoo.http import request


class Main(http.Controller):

    @http.route('/sign_in', type='http', auth="public", website=True)
    def sign_in(self, **kw):
        country_ids = request.env['res.country'].search([])

        return request.render(
            'barbershop.sign_in',
            {
                'default_name': 'Jesus',
                'country_list': country_ids,
            }
        )
