{
    'name': 'Barbería',
    'category': 'Curso',
    'version': '16.0.0.0.0',
    'license': 'AGPL-3',
    'author': 'Iciva Technology',
    'depends': [
        'contacts',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/barbershop_security.xml',
        'data/barbershop_state_data.xml',
        'views/barbershop_appointment_views.xml',
        'views/barbershop_service_views.xml',
        'views/barbershop_menu.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        ],
    },
    'application': True,
    'installable': True,
}
