from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError
import random
import logging

_logger = logging.getLogger(__name__)

class javv_vehiculos(models.Model):
    _name = 'javv.vehiculos'
    _description = 'Gestión básica de vehículos'
    _order = "codigo asc"

    @api.model
    def init(self):
        _logger.info("Cargando el modelo javv.vehiculos correctamente...")
        super(javv_vehiculos, self).init()

    name = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código", required=True, copy=False, default=lambda self: self._generate_codigo())
    matricula = fields.Char(string="Matrícula", required=True)
    fecha_fabricacion = fields.Date(string="Fecha de Fabricación")
    potencia = fields.Float(string="Potencia (CV)", help="Potencia del vehículo en caballos de vapor")
    neumaticos_id = fields.Many2one(
        'javv.neumaticos',
        string="Neumáticos",
        required=False,
        help="Selecciona el neumático del vehículo o crea uno nuevo."
    )



    fecha_itv = fields.Date(string="Fecha de ITV", compute="_compute_fecha_itv", store=True)

    @staticmethod
    def _generate_codigo():
        from datetime import datetime
        current_date = datetime.now().strftime("%d%m%Y")
        user_id = random.randint(1, 999)  # Usamos un identificador simulado
        return f"{user_id}-{current_date}"

    @api.depends('fecha_fabricacion')
    def _compute_fecha_itv(self):
        for record in self:
            if record.fecha_fabricacion:
                record.fecha_itv = record.fecha_fabricacion + timedelta(days=6 * 365)
            else:
                record.fecha_itv = False


    tipo_vehiculo_id = fields.Many2one('javv.tipos_vehiculos', string="Tipo de vehículo")
    caracteristicas_ids = fields.Many2many(
        'javv.caracteristicas_vehiculos',
        string="Características especiales"
    )
    combustible = fields.Selection([
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diésel'),
        ('gas', 'Gas'),
        ('hibrido', 'Híbrido'),
        ('electrico', 'Eléctrico')
    ], string="Combustible")
    num_plazas = fields.Integer(string="Número de Plazas", default=5)
    precio_diario = fields.Float(string="Precio Diario")
    precio_semanal = fields.Float(string="Precio Semanal", compute="_compute_precio_semanal", store=True)

    @api.depends('precio_diario')
    def _compute_precio_semanal(self):
        for record in self:
            if record.precio_diario and record.precio_diario > 0:
                record.precio_semanal = record.precio_diario * 5  # Multiplicación por días laborales
            else:
                record.precio_semanal = 1  # Establezco un valor mínimo por defecto para evitar conflictos

    state = fields.Selection([
        ('disponible', 'Disponible'),
        ('alquilado', 'Alquilado'),
        ('en_reparacion', 'En Reparación')
    ], string="Estado", default='disponible', readonly=True)

    decoration_state = fields.Char(compute="_compute_decoration_state", string="Decoration State")

    def _compute_decoration_state(self):
        for record in self:
            if record.state == 'disponible':
                record.decoration_state = 'success'
            elif record.state == 'alquilado':
                record.decoration_state = 'success_bold'
            elif record.state == 'en_reparacion':
                record.decoration_state = 'danger_italic'

    _sql_constraints = [
        ('unique_matricula', 'unique(matricula)', 'La matrícula debe ser única.'),
        ('check_num_plazas', 'CHECK(num_plazas > 0)', 'El número de plazas debe ser mayor que cero.'),
        ('check_precio_diario', 'CHECK(precio_diario > 0)', 'El precio diario debe ser mayor que cero.'),
        ('check_capacidad_maletero', 'CHECK(capacidad_maletero >= 0)', 'La capacidad del maletero debe ser positiva.'),
        ('check_potencia', 'CHECK(potencia > 0)', 'La potencia debe ser mayor que cero.'),
    ]

    def action_comenzar_reparacion(self):
        for record in self:
            if record.state != 'disponible':
                raise ValidationError('Solo los vehículos en estado "Disponible" pueden iniciar reparación.')
            record.state = 'en_reparacion'

    def action_terminar_reparacion(self):
        for record in self:
            if record.state != 'en_reparacion':
                raise ValidationError('Solo los vehículos en estado "En Reparación" pueden terminar reparación.')
            record.state = 'disponible'

    numero_alquileres = fields.Integer(
        string="Número de Alquileres",
        compute="_compute_numero_alquileres",
        store=True,
        readonly=True
    )
    maletero = fields.Boolean(string="¿Tiene maletero?")
    capacidad_maletero = fields.Float(string="Capacidad del Maletero", default=0)

    # Métodos compute
    @api.depends('alquileres_ids')
    def _compute_numero_alquileres(self):
        for record in self:
            record.numero_alquileres = len(record.alquileres_ids)

    @api.onchange('maletero')
    def _onchange_maletero(self):
        for record in self:
            if record.maletero:
                record.capacidad_maletero = 300
            else:
                record.capacidad_maletero = 0

    @api.constrains('maletero', 'capacidad_maletero')
    def _check_capacidad_maletero(self):
        for record in self:
            if record.maletero and record.capacidad_maletero <= 0:
                raise ValidationError('La capacidad del maletero debe ser mayor que 0 si el vehículo tiene maletero.')

    # Relación con alquileres
    alquileres_ids = fields.One2many(
        'javv.alquileres_vehiculos',
        'vehiculo_id',
        string="Alquileres Asociados"
    )