from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError

class javv_inmuebles(models.Model):
    _name = "javv.propiedades_inmuebles"  # Se creará una tabla llamada javv_inmuebles
    _description = "Propiedades Inmuebles"

    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")
    cliente_id = fields.Many2one("res.partner", string="Comprador", copy=False)
    agente_id = fields.Many2one("res.users", string="Vendedor", default=lambda self: self.env.user)
    tipos_id = fields.Many2one("javv.tipos_inmuebles", string="Tipo")
    etiquetas_ids = fields.Many2many("javv.etiquetas_inmuebles", string="Etiquetas")
    ofertas_ids = fields.One2many("javv.ofertas_inmuebles", "inmueble_id", string="Ofertas")
    codigo_postal = fields.Char(string="Código Postal")
    fecha_disponibilidad = fields.Date(
        string="Fecha de Disponibilidad",
        copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    precio_esperado = fields.Float(string="Precio Esperado", required=True)
    precio_venta = fields.Float(string="Precio de Venta", readonly=True, copy=False)
    dormitorios = fields.Integer(string="Nº Dormitorios", default=2)
    salon = fields.Integer(string="Tamaño del Salón")
    fachadas = fields.Integer(string="Nº Fachadas")
    garage = fields.Boolean(string="Garage")
    jardin = fields.Boolean(string="Jardín")
    area_jardin = fields.Integer(string="Tamaño del Jardín m²")
    orientacion_jardin = fields.Selection(
        [('norte', 'Norte'), ('sur', 'Sur'), ('este', 'Este'), ('oeste', 'Oeste')],
        string="Orientación del Jardín"
    )
    active = fields.Boolean(string="Activo", default=True)
    state = fields.Selection([
        ('nuevo', 'Nuevo'),
        ('oferta_recibida', 'Oferta Recibida'),
        ('oferta_aceptada', 'Oferta Aceptada'),
        ('vendido', 'Vendido'),
        ('cancelado', 'Cancelado')
    ], string="Estado", required=True, copy=False, default="nuevo")

    # Campo calculado para el área total
    area_total = fields.Integer(
        compute="_calcular_area_total",
        search="_search_area_total",
        store=True,  # Para almacenar el valor en la base de datos
        string="Área total (m²)"
    )

    @api.depends("salon", "area_jardin")
    def _calcular_area_total(self):
        for record in self:
            record.area_total = (record.salon or 0) + (record.area_jardin or 0)

    def _search_area_total(self, operator, value):
        return [('area_total', operator, value)]

    # Campo calculado para la mejor oferta
    mejor_oferta = fields.Float(compute="_calcular_mejor_oferta", string="Mejor Oferta", store=True)

    @api.depends("ofertas_ids.precio")
    def _calcular_mejor_oferta(self):
        for record in self:
            if record.ofertas_ids:
                record.mejor_oferta = max(record.ofertas_ids.mapped("precio"))
            else:
                record.mejor_oferta = 0


    # Metodo Onchange para el campo 'jardin'
    @api.onchange("jardin")
    def _onchange_jardin(self):
        if self.jardin:
            self.area_jardin = 10
            self.orientacion_jardin = 'norte'
        else:
            self.area_jardin = 0
            self.orientacion_jardin = ''

    # MÉTODOS PARA BOTONES
    def action_vender_propiedad(self):
        for record in self:
            if record.state == 'cancelado':
                raise UserError("Las propiedades canceladas no pueden ser vendidas.")
            record.state = 'vendido'

    def action_cancelar_propiedad(self):
        for record in self:
            if record.state == 'vendido':
                raise UserError("Las propiedades vendidas no pueden ser canceladas.")
            record.state = 'cancelado'