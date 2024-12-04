from odoo import fields, models

class javv_tipos_inmuebles(models.Model):
    _name = "javv.tipos_inmuebles"
    _description = "Modelo (tabla) para los tipos de propiedades inmobiliarias"

    name = fields.Char("Nombre", required=True)
