from odoo import fields, models

class javv_alquileres_vehiculos(models.Model):
    _name = 'javv.alquileres_vehiculos'
    _description = 'Alquileres de Vehículos'

    # Campos básicos
    fecha_inicio = fields.Date(string="Fecha de Inicio", required=True, default=fields.Date.today)
    fecha_fin = fields.Date(string="Fecha de Fin")
    duracion = fields.Integer(string="Duración (días)")
    precio_final = fields.Float(string="Precio Final")
    state = fields.Selection([
        ('previo', 'Previo'),
        ('en_proceso', 'En Proceso'),
        ('terminado', 'Terminado'),
        ('facturado', 'Facturado'),
        ('cancelado', 'Cancelado')
    ], string="Estado", default='previo', required=True)

    # Relaciones
    vehiculo_id = fields.Many2one('javv.vehiculos', string="Vehículo", required=True)
    usuario_id = fields.Many2one('res.users', string="Usuario que gestiona", default=lambda self: self.env.user)
    cliente_id = fields.Many2one('res.partner', string="Cliente", required=True)
