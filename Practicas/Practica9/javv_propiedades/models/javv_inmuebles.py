from odoo import fields, models
from datetime import timedelta

class javv_inmuebles(models.Model):
    _name = "javv.propiedades_inmuebles"  # Se creará una tabla llamada javv_inmuebles
    _description = "Propiedades Inmuebles"

    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")
    cliente_id = fields.Many2one("res.partner", string="Comprador", copy=False)
    agente_id = fields.Many2one("res.users", string="Vendedor", default=lambda self: self.env.user)
    tipos_id = fields.Many2one("javv.tipos_inmuebles", string="Tipo")
    codigo_postal = fields.Char(string="Código Postal")
    fecha_disponibilidad = fields.Date(string="Fecha de Disponibilidad",
                                       copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    precio_esperado = fields.Float(string="Precio Esperado", required=True)
    precio_venta = fields.Float(string="Precio de Venta", readonly=True, copy=False)
    dormitorios = fields.Integer(string="Nº Dormitorios", default=2)
    salon = fields.Integer(string="Tamaño del Salón")
    fachadas = fields.Integer(string="Nº Fachadas")
    garage = fields.Boolean(string="Garage")
    jardin = fields.Boolean(string="Jardín")
    area_jardin = fields.Integer(string="Tamaño del Jardín m²")
    orientacion_jardin = fields.Selection([('norte', 'Norte'), ('sur', 'Sur'),
                                           ('este', 'Este'), ('oeste', 'Oeste')],
                                          string="Orientación del Jardín")
    active = fields.Boolean(string="Activo", default=True)
    state = fields.Selection([('nuevo', 'Nuevo'), ('oferta_recibida', 'Oferta Recibida'),
                               ('oferta_aceptada', 'Oferta Aceptada'),
                               ('vendido', 'Vendido'), ('cancelado', 'Cancelado')],
                              string="Estado", required=True, copy=False, default="nuevo")