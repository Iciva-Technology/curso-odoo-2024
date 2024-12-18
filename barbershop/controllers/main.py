from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class Main(http.Controller):

    @http.route('/sign_in', type='http', auth="public", website=True)
    def sign_in(self, **kw):
        country_ids = request.env['res.country'].search([])

        return request.render(
            'barbershop.sign_in',
            {
                'default_name': '',
                'country_list': country_ids,
            }
        )

    @http.route('/reservation', type='http', auth="public", website=True)
    def reservation(self, **kw):
        partner_id = request.env['res.partner'].search([])
        service_ids = request.env['barbershop.service'].search([])
        employee_id = request.env['hr.employee'].search([])


        return request.render(
            'barbershop.reservation',
            {
                'partner_list': partner_id,
                'service_list': service_ids,
                'employee_list': employee_id,
            }
        )
    
    @http.route('/create_appointment', type='json', auth='public')
    def create_appointment(self, data, **kw):
        try:
            # Extraer datos del JSON
            partner_id = int(data.get('partner_id'))
            service_id = int(data.get('service_id'))
            employee_id = int(data.get('employee_id'))
            start_at = data.get('start_at')

            # Validar los datos
            if not partner_id or not service_id or not employee_id or not start_at:
                return {'error': 'Todos los campos son obligatorios.'}

            # Convertir las fechas
            start_at = datetime.strptime(start_at, '%Y-%m-%dT%H:%M')  # Formato HTML5 para datetime-local

            # Crear el registro en barbershop.appointment
            request.env['barbershop.appointment'].sudo().create({
                'partner_id': partner_id,
                'start_at': start_at,
                'service_ids': [(4, service_id)],
                'barber_id': employee_id,
            })

            return {'success': True}

        except ValidationError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': 'Ocurrió un error al procesar la cita.'}
        