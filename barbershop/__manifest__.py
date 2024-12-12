{
    'name': 'Barbería',
    'category': 'Curso',
    'version': '16.0.0.0.0',
    'license': 'AGPL-3',
    'author': 'Iciva Technology',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/barbershop_appointment_views.xml',
        'views/barbershop_service_views.xml',
        'views/barbershop_menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        ],
    },
    'application': True,
    'installable': True,
}
