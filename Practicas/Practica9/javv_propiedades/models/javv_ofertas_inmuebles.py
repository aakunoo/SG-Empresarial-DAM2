from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import timedelta, date

class javv_ofertas_inmuebles(models.Model):
    _name = "javv.ofertas_inmuebles"
    _description = "Modelo (tabla) para las ofertas de compra de propiedades inmobiliarias"

    precio = fields.Float(string="Precio", required=True)
    estado = fields.Selection(
        [('nueva', 'Nueva'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')],
        string="Estado",
        default="nueva",
        copy=False
    )
    comprador_id = fields.Many2one("res.partner", string="Comprador", required=True)
    inmueble_id = fields.Many2one("javv.propiedades_inmuebles", string="Propiedad", required=True)

    validez = fields.Integer(default=7, string="Validez (días)")
    fecha_tope = fields.Date(compute="_calcular_fecha_tope", inverse="_inverso_fecha_tope", string="Fecha Tope")


    @api.depends("validez")
    def _calcular_fecha_tope(self):
        for record in self:
            if record.create_date:
                record.fecha_tope = record.create_date + timedelta(days=record.validez)
            else:
                record.fecha_tope = date.today() + timedelta(days=record.validez)

    def _inverso_fecha_tope(self):
        for record in self:
            record.validez = (record.fecha_tope - date.today()).days if record.fecha_tope else 0


    def action_aceptar_oferta(self):
        for record in self:
            if record.estado == 'aceptada':
                raise UserError("La oferta ya ha sido aceptada.")
            record.estado = 'aceptada'
            record.inmueble_id.precio_venta = record.precio
            record.inmueble_id.cliente_id = record.comprador_id
            record.inmueble_id.state = 'oferta_aceptada'

    def action_rechazar_oferta(self):
        for record in self:
            if record.estado == 'rechazada':
                raise UserError("La oferta ya ha sido rechazada.")
            record.estado = 'rechazada'
