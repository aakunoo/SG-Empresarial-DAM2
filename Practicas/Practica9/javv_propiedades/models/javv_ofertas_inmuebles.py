from odoo import fields, models

class javv_ofertas_inmuebles(models.Model):
    _name = "javv.ofertas_inmuebles"
    _description = "Modelo (tabla) para las ofertas de compra de propiedades inmobiliarias"

    precio = fields.Float(string="Precio", required=True)
    estado = fields.Selection([('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], string="Estado", copy=False)
    comprador_id = fields.Many2one("res.partner", string="Comprador", required=True)
    inmueble_id = fields.Many2one("javv.propiedades_inmuebles", string="Propiedad", required=True)
