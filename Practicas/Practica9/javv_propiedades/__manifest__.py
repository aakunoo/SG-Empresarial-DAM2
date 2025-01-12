{
    'name': 'javv_propiedades',
    'summary': 'Módulo de gestión de propiedades inmobiliarias.',
    'description': 'Propiedades Inmobiliarias',
    'author': 'Jeronimo',
    'depends': ['base'],
    'data': [
        'views/javv_propiedades_inmuebles_views.xml',
        'views/javv_inmuebles_ofertas_views.xml',
        'views/javv_tipos_views.xml',
        'views/javv_inmuebles_etiquetas_views.xml',
        'views/javv_propiedades_menus.xml',
        'views/javv_res_users_views.xml',
        'reports/javv_propiedades_inmuebles_reports.xml',
        'reports/javv_propiedades_inmuebles_templates.xml',
        'reports/javv_res_users_reports.xml',
        'reports/javv_res_users_templates.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
}