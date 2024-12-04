{
    'name': 'javv_propiedades',
    'summary': 'Módulo de gestión de propiedades inmobiliarias.',
    'description': 'Propiedades Inmobiliarias',
    'author': 'Jeronimo',
    'depends': ['base'],
    'data': [
        'views/javv_propiedades_inmuebles_views.xml',
        'views/javv_tipos_views.xml',
        'views/javv_propiedades_menus.xml',
        'security/ir.model.access.csv',
],
    'application': True,
}