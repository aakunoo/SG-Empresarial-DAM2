from odoo import fields, models

class javv_vehiculos(models.Model):
    _name = 'javv.vehiculos'
    _description = 'Gestión básica de vehículos'

    name = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código", required=True, copy=False)
    matricula = fields.Char(string="Matrícula", required=True)
    tipo_vehiculo_id = fields.Many2one('javv.tipos_vehiculos', string="Tipo de vehículo")
    caracteristicas_ids = fields.Many2many(
        'javv.caracteristicas_vehiculos',
        string="Características especiales"
    )
