from odoo import models, fields


class javv_caracteristicas_vehiculos(models.Model):
    _name = 'javv.caracteristicas_vehiculos'
    _description = 'Características especiales de vehículos'
    _order = "sequence, name asc"

    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string="Color")
    sequence = fields.Integer(string="Secuencia", default=10)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'El nombre de la característica debe ser único.')
    ]
