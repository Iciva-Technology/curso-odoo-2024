from odoo import http
from odoo.http import request
from datetime import datetime
import uuid
import logging
import pytz

# Creamos el logger específico para este controlador
_logger = logging.getLogger(__name__)

def format_start_at_for_odoo(start_at):
    """
    Convierte una fecha con formato ISO (2024-12-19T13:17) al formato de Odoo (2024-12-19 13:17)
    
    Args:
        start_at (str): Fecha en formato ISO con 'T' como separador
        
    Returns:
        str: Fecha formateada para Odoo
    """
    try:
        # Convertir el formato con 'T' al formato que Odoo espera
        dt = datetime.strptime(start_at, '%Y-%m-%dT%H:%M')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M')
        return formatted_date
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
        
    @http.route('/make_appointment/sent', type='json', auth='public', methods=['POST'])
    def make_appointment_sent(self, data, **kw):
        try:
            # Log al inicio de la petición
            _logger.info('Iniciando petición POST appointment con datos: %s', data)
            
            start_at = start_at.replace('T', ' ') #format_start_at_for_odoo(data.get('start_at'))
            
            # Log de los datos procesados
            _logger.debug('Datos a procesar: %s', data)
            _logger.debug('Fecha formateada: %s', start_at)
            
            try:
                # Creamos el registro
                appointment = request.env['barbershop.appointment'].sudo().create({
                    'name': uuid.uuid4(),
                    'start_at': start_at,
                    'service_ids': [(6, 0, [int(x) for x in data['service_ids']])],
                    'partner_id': data.get('partner_id'),
                    'barber_id': data.get('barber_id')
                })
                _logger.info('Cita creada exitosamente con ID: %s', appointment.id)
                
            except Exception as db_error:
                _logger.error('Error al crear la cita en la base de datos: %s', str(db_error))
                raise
            
            # Log de respuesta exitosa
            _logger.debug('Enviando respuesta exitosa para appointment_id: %s', appointment.id)
            return {
                'success': True,
                'appointment_id': appointment.id,
                'message': 'Cita creada exitosamente'
            }
            
        except Exception as e:
            # Log de error general
            _logger.error('Error general en make_appointment_sent: %s', str(e), exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
