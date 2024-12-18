{
    'name': 'javv_modulo_vehiculos',
    'summary': 'Gestión básica de vehículos.',
    'description': 'Módulo de prueba con el modelo principal de vehículos.',
    'author': 'Jerónimo Álvaro Vicente Vidal',
    'depends': ['base'],  # Depende del módulo base
    'data': [
        'security/ir.model.access.csv',
        'views/javv_caracteristicas_vehiculos_views.xml',  # Primero características
        'views/javv_tipos_vehiculos_views.xml',  # Luego tipos
        'views/javv_vehiculos_views.xml',  # Ahora vehículos
        'views/javv_alquileres_vehiculos_views.xml',
        'views/javv_menus.xml',
    ],
    'application': True,
}
