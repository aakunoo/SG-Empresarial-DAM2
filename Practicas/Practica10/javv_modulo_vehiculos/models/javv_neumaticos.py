from odoo import fields, models

class javv_neumaticos(models.Model):
    _name = 'javv.neumaticos'
    _description = 'Tipos de Neumáticos'

    name = fields.Char(string="Nombre del Neumático", required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'El nombre del neumático debe ser único.')
    ]
