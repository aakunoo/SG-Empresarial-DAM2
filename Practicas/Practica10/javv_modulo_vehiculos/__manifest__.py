{
    'name': 'Alquiler de Vehiculos',
    'summary': 'Gestión básica de vehículos.',
    'description': 'Módulo de prueba con el modelo principal de vehículos.',
    'author': 'Jerónimo Álvaro Vicente Vidal',
    'license': 'LGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/javv_caracteristicas_vehiculos_views.xml',
        'views/javv_tipos_vehiculos_views.xml',
        'views/javv_vehiculos_views.xml',
        'views/javv_alquileres_vehiculos_views.xml',
        'views/javv_menus.xml',
        'views/javv_herencia_views.xml',
        'data/javv_neumaticos_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'javv_modulo_vehiculos/static/src/css/alquileres.css',
        ],
    },
    'application': True,
}
