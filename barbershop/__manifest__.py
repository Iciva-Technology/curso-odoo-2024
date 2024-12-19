{
    'name': 'Barbería',
    'category': 'Curso',
    'version': '16.0.0.0.0',
    'license': 'AGPL-3',
    'author': 'Iciva Technology',
    'depends': [
        'contacts',
        'hr',
        'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/barbershop_security.xml',
        'data/barbershop_state_data.xml',
        'data/request_validators/barbershop_appoiment.xml',
        'data/request_validators/res_partner_data.xml',
        'views/barbershop_appointment_views.xml',
        'views/barbershop_service_views.xml',
        'views/barbershop_menu.xml',
        'views/res_partner_views.xml',
        'views/web/sign_up.xml',
        'views/web/make_appoiment.xml',
        'views/web/appointment_consultation.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            'barbershop/static/src/**/*',
        ],
    },
    'application': True,
    'installable': True,
}
