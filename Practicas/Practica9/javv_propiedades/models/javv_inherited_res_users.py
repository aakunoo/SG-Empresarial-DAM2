from odoo import fields, models

class javv_inherited_res_users(models.Model):
    _inherit = "res.users"

    # Campo para enlazar con las propiedades asignadas al usuario
    javv_propiedades_ids = fields.One2many(
        "javv.propiedades_inmuebles",  # Relación con el modelo de propiedades
        "javv_agente_id",             # Campo inverso en el modelo de propiedades
        string="Propiedades Asignadas"
    )