from odoo import fields, models
from datetime import timedelta

class javv_inmuebles(models.Model):
    _name = "javv.propiedades_inmuebles"
    _description = "Propiedades Inmuebles"

    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")
    cogigo_postal = fields.Char(string="Código Postal")
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