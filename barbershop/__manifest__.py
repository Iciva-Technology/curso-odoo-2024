{
    'name': 'Barbería',
    'category': 'Curso',
    'version': '16.0.0.0.0',
    'license': 'AGPL-3',
    'author': 'Iciva Technology',
    'depends': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/customer.xml',
        'views/barbershop_appointment_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        ],
    },
    'application': True,
    'installable': True,
}
