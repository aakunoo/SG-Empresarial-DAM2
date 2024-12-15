{
    'name': 'javv_modulo_vehiculos',
    'summary': 'Gestión básica de vehículos.',
    'description': 'Módulo de prueba con el modelo principal de vehículos.',
    'author': 'Jerónimo Álvaro Vicente Vidal',
    'depends': ['base'],  # Depende del módulo base
    'data': [
        'security/ir.model.access.csv',  # Permisos
        'views/javv_vehiculos_views.xml',  # Define la acción
        'views/javv_menus.xml',  # Define el menú que usa la acción
    ],
    'application': True,
}
