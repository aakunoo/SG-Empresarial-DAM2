from odoo import models, fields

class javv_herencia(models.Model):
    _inherit = 'res.partner'

    alquileres_ids = fields.One2many(
        comodel_name='javv.alquileres_vehiculos',
        inverse_name='cliente_id',
        string='Alquileres de Vehículos'
    )
