from odoo import http
from odoo.http import request
import logging



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
    
    @http.route('/appointment_consultation', type='http', auth="public", website=True)
    def appointment_consultation(self, **kw):
        return request.render(
            'barbershop.appointment_consultation',
        )

    @http.route('/get_appointment_details', type='json', auth='public', methods=['POST'])
    def get_appointment_details(self, appointment_number):
        appointment = request.env['barbershop.appointment'].sudo().search([('name', '=', appointment_number)], limit=1)
        _logger.info(f'\n\n\n\n\n {appointment} \n\n\n\n\n\n')
        if appointment:
            return {
                'success': True,
                'details': {
                    'client': appointment.name,
                }
            }
        else:
            return {'success': False}