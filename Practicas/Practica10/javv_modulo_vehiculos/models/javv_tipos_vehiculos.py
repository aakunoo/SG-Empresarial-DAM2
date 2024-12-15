from odoo import models, fields

class javv_tipos_vehiculos(models.Model):
    _name = 'javv.tipos_vehiculos'
    _description = 'Tipos de vehículos'

    name = fields.Char(string="Nombre", required=True)
    clasificacion_energetica = fields.Selection([
        ('0', '0'),
        ('eco', 'Eco'),
        ('c', 'C'),
        ('b', 'B'),
        ('sin_clasificar', 'Sin clasificar')
    ], string="Clasificación energética", default='sin_clasificar')
    enganche_carro = fields.Boolean(string="Enganche para carro", default=False)
