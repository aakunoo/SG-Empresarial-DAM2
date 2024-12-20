from odoo import models, fields, api
from odoo.exceptions import ValidationError

class javv_tipos_vehiculos(models.Model):
    _name = 'javv.tipos_vehiculos'
    _description = 'Tipos de vehículos'

    name = fields.Char(string="Nombre", required=True)
    clasificacion_energetica = fields.Selection([
        ('0', '0'),
        ('eco', 'Eco'),
        ('c', 'C'),
        ('b', 'B'),
        ('sin_clasificar', 'Sin clasificar')
    ], string="Clasificación energética", default='sin_clasificar')
    enganche_carro = fields.Boolean(string="Enganche para carro", default=False)

    @api.constrains('enganche_carro')
    def _check_enganche(self):
        for record in self:
            vehiculos = self.env['javv.vehiculos'].search([('tipo_vehiculo_id', '=', record.id)])
            for vehiculo in vehiculos:
                if record.enganche_carro and vehiculo.num_plazas < 4:
                    raise ValidationError('Los vehículos con enganche para carro deben tener al menos 4 plazas.')
