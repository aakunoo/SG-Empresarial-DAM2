from odoo import fields, models, api

class javv_tipos_inmuebles(models.Model):
    _name = "javv.tipos_inmuebles"
    _description = "Modelo (tabla) para los tipos de propiedades inmobiliarias"
    _order = "secuencia"

    name = fields.Char("Nombre", required=True)
    secuencia = fields.Integer('Secuencia')
    inmuebles_ids = fields.One2many(
        "javv.propiedades_inmuebles",
        "tipos_id",
        string="Propiedades Inmuebles"
    )

    ofertas_ids = fields.One2many(
        "javv.ofertas_inmuebles",
        "tipo_propiedad_id",
        string="Ofertas"
    )

    # Campo computado para contar ofertas
    contador_ofertas = fields.Integer(
        compute="_calcular_numero_ofertas",
        string="Número de Ofertas"
    )

    _sql_constraints = [
        ('check_name', 'unique(name)', 'El nombre del TIPO DE PROPIEDAD debe ser único.')
    ]

    @api.depends("ofertas_ids")
    def _calcular_numero_ofertas(self):
        for record in self:
            record.contador_ofertas = len(record.ofertas_ids)

