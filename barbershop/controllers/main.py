from odoo import http
from odoo.http import request
from datetime import datetime
import uuid
import logging
import json
import pytz

# Creamos el logger específico para este controlador
_logger = logging.getLogger(__name__)

def format_start_at_for_odoo(start_at):
    """
    Convierte una fecha con formato ISO (2024-12-19T13:17) al formato de Odoo (2024-12-19 13:17:00)
    """
    try:
        dt = datetime.strptime(start_at, '%Y-%m-%dT%H:%M')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        raise ValueError(f"Error al formatear la fecha: {str(e)}")

# Ejemplo de uso:
# fecha_entrada = '2024-12-19T13:09'
# fecha_formateada = format_datetime_for_odoo(fecha_entrada)
# print(fecha_formateada)  # Output: '2024-12-19 13:09'

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
        
    @http.route('/make_appoiment', type='http', auth="public", csrf=True, website=True)
    def make_appointment(self, **kw):
        partners = request.env['res.partner'].search([])
        barbers = request.env['hr.employee'].search([])
        services = request.env['barbershop.service'].search([])

        return request.render(
            'barbershop.make_appoiment',
            {
                'partner_list': partners,
                'barber_list': barbers,
                'service_list': services,
            }
        )
        
    @http.route('/make_appointment/sent', type='http', auth='public', methods=['POST'], website=True)
    def make_appointment_sent(self, data, **kw):
        try:
            # Log inicial de la petición
            _logger.info('Iniciando petición POST appointment con datos: %s', data)
            
            # Procesar y formatear los datos
            start_at = format_start_at_for_odoo(data.get('start_at'))
            partner_id = int(data.get('partner_id'))
            barber_id = int(data.get('barber_id'))
            service_ids = [(6, 0, [int(x) for x in data.get('service_ids', [])])]
            
            # Crear el registro
            appointment = request.env['barbershop.appointment'].sudo().create({
                'name': str(uuid.uuid4()),
                'start_at': start_at,
                'service_ids': service_ids,
                'partner_id': partner_id,
                'barber_id': barber_id,
            })
            
            # Log de éxito
            _logger.info('Cita creada exitosamente con ID: %s', appointment.id)
            return {
                'success': True,
                'appointment_id': appointment.id,
                'message': 'Cita creada exitosamente'
            }
        
        except Exception as e:
            # Log de error
            _logger.error('Error general en make_appointment_sent: %s', str(e), exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
            
    @http.route('/make_appointment/get', type='http', auth='public', methods=['GET'], csrf=False)
    def get_appointments(self):
        appointments = request.env['barbershop.appointment'].sudo().search([])
        data = [
            {
                'id': appointment.id,
                'partner_id': appointment.partner_id.name,
                'barber_id': appointment.barber_id.name,
                'start_at': appointment.start_at,
                'service_ids': [service.name for service in appointment.service_ids],
            }
            for appointment in appointments
        ]
        return http.Response(
            json.dumps(data),
            content_type='application/json',
            status=200
        )
