from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class javv_inmuebles(models.Model):
    _name = "javv.propiedades_inmuebles"  # Se creará una tabla llamada javv_inmuebles
    _description = "Propiedades Inmuebles"
    _order = "id desc"

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

    area_total = fields.Integer(
        compute="_calcular_area_total",
        search="_search_area_total",
        store=True,
        string="Área total (m²)"
    )

    javv_agente_id = fields.Many2one(
        "res.users",
        string="Agente Responsable"
    )

    @api.depends("salon", "area_jardin")
    def _calcular_area_total(self):
        for record in self:
            record.area_total = (record.salon or 0) + (record.area_jardin or 0)

    def _search_area_total(self, operator, value):
        return [('area_total', operator, value)]

    mejor_oferta = fields.Float(compute="_calcular_mejor_oferta", string="Mejor Oferta", store=True)

    @api.depends("ofertas_ids.precio")
    def _calcular_mejor_oferta(self):
        for record in self:
            if record.ofertas_ids:
                record.mejor_oferta = max(record.ofertas_ids.mapped("precio"))
            else:
                record.mejor_oferta = 0

    @api.onchange("jardin")
    def _onchange_jardin(self):
        if self.jardin:
            self.area_jardin = 10
            self.orientacion_jardin = 'norte'
        else:
            self.area_jardin = 0
            self.orientacion_jardin = ''

    def action_vender_propiedad(self):
        for record in self:
            if record.state in ['vendido', 'cancelado']:
                raise UserError("No se puede vender una propiedad que ya está vendida o cancelada.")
            record.state = 'vendido'

    def action_cancelar_propiedad(self):
        for record in self:
            if record.state in ['vendido', 'cancelado']:
                raise UserError("No se puede cancelar una propiedad que ya está vendida o cancelada.")
            record.state = 'cancelado'

    _sql_constraints = [
        ('check_precio_esperado', 'CHECK(precio_esperado > 0)',
         'El valor del PRECIO ESPERADO debe ser estrictamente positivo.')
    ]

    @api.constrains('precio_venta', 'precio_esperado')
    def _check_precio_venta(self):
        for record in self:
            if float_is_zero(record.precio_venta, 2):
                continue
            if float_compare(record.precio_venta, (record.precio_esperado * 0.9), 2) == -1:
                raise ValidationError(
                    "EL PRECIO DE VENTA debe ser, al menos, del 90% del PRECIO ESPERADO. "
                    "Puede reducir el PRECIO ESPERADO para aceptar esta oferta.")

    def action_ver_campos(self):
        cadena = "Inmuebles\n"

        for record in self:
            cadena += "Nombre: " + str(record.name) + "\n"
            cadena += "Precio esperado: " + str(record.precio_esperado) + "\n"
            cadena += "Tipo: " + (record.tipos_id.name or "Sin tipo") + "\n"

        if len(self) > 0:
            media_dorm = sum(self.mapped("dormitorios")) / len(self)
            cadena += "Media de dormitorios: " + str(media_dorm) + "\n"

        cadena += "\nEtiquetas\n"

        etiquetas = self.env["javv.etiquetas_inmuebles"].browse([1, 5, 6])
        for etiqueta in etiquetas:
            cadena += "Nombre: " + str(etiqueta.name) + "\n"
            cadena += "Color: " + str(etiqueta.color) + "\n"
        raise UserError(cadena)

    def action_modificar_campos(self):
        for record in self:
            record.jardin = False

        ofertas = self.env["javv.ofertas_inmuebles"].browse([3, 4])
        for oferta in ofertas:
            oferta.validez = 10

    def action_ver_entorno(self):
        cadena = ""
        cadena += "Usuario actual: " + str(self.env.user.name) + "\n"
        cadena += "Compañía actual: " + str(self.env.company.name) + "\n"
        cadena += "Identificador de usuario (uid): " + str(self.env.uid) + "\n"

        vista_tree = self.env.ref("javv_propiedades.javv_propiedades_inmuebles_view_tree")
        cadena += "Registro de la vista de lista: " + str(vista_tree) + "\n"
        cadena += "Bandeira de superusuario: " + str(self.env.su) + "\n"
        cadena += "Código de lenguaje: " + str(self.env.lang) + "\n"

        self.env.lang = "es_ES"
        cadena += "\nTras modificarlo, el nuevo lang es: " + str(self.env.lang)

        raise UserError(cadena)

    def action_modificar_entorno(self):
        record2 = self.with_user(1)
        record2 = record2.with_company(2)
        record2 = record2.sudo(True)

        cadena = ""
        cadena += "Usuario actual: " + str(record2.env.user.name) + "\n"
        cadena += "Compañía actual: " + str(record2.env.company.name) + "\n"
        cadena += "Bandera de superusuario: " + str(record2.env.su) + "\n"

        raise UserError(cadena)

    def action_sql(self):
        sentencia = """
            INSERT INTO javv_propiedades_inmuebles
            (name, precio_esperado, dormitorios, state, active)
            VALUES ('Piso en Zamora', 100000, 5, 'nuevo', True)
        """
        self.env.cr.execute(sentencia)
        self.env.cr.commit()

        dormitorios = 3
        query = """
            SELECT id, name, codigo_postal
            FROM javv_propiedades_inmuebles
            WHERE dormitorios = %s
            ORDER BY id
        """ % (dormitorios,)

        self.env.cr.execute(query)
        resultado = self.env.cr.fetchall()

        cadena = ""
        for inmueble in resultado:
            cadena += "id: " + str(inmueble[0]) + " + nombre: " + str(inmueble[1]) + \
                      " + código postal: " + str(inmueble[2]) + "\n"
        raise UserError(cadena)