from odoo import fields, models

class javv_vehiculos(models.Model):
    _name = 'javv.vehiculos'
    _description = 'Gestión básica de vehículos'

    name = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código", required=True, copy=False)
    matricula = fields.Char(string="Matrícula", required=True)
    fecha_fabricacion = fields.Date(string="Fecha de Fabricación")
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
    precio_semanal = fields.Float(string="Precio Semanal")
    state = fields.Selection([
        ('disponible', 'Disponible'),
        ('alquilado', 'Alquilado'),
        ('en_reparacion', 'En Reparación')
    ], string="Estado", default='disponible', readonly=True)