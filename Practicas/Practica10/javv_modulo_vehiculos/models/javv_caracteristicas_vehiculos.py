from odoo import models, fields


class javv_caracteristicas_vehiculos(models.Model):
    _name = 'javv.caracteristicas_vehiculos'
    _description = 'Características especiales de vehículos'

    name = fields.Char(string="Nombre", required=True)
