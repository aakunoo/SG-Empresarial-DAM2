from odoo import fields, models

class javvEtiquetasInmuebles(models.Model):
    _name = "javv.etiquetas_inmuebles"
    _description = "Modelo (tabla) para las etiquetas que califican las propiedades inmobiliarias"

    name = fields.Char(string="Nombre", required=True)