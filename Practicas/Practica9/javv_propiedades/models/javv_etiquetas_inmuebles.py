from odoo import fields, models

class javv_etiquetas_inmuebles(models.Model):
    _name = "javv.etiquetas_inmuebles"
    _description = "Modelo (tabla) para las etiquetas que califican las propiedades inmobiliarias"
    _order = "name"

    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('check_name', 'unique(name)', 'El nombre de la ETIQUETA DE PROPIEDAD debe ser único.')
    ]