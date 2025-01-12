from odoo import models, fields, api
from odoo.exceptions import ValidationError

class javv_tipos_vehiculos(models.Model):
    _name = 'javv.tipos_vehiculos'
    _description = 'Tipos de vehículos'
    _order = "name asc"

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

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'El nombre del tipo de vehículo debe ser único.')
    ]

    vehiculos_ids = fields.One2many(
        'javv.vehiculos', 'tipo_vehiculo_id', string="Vehículos Relacionados"
    )

    def action_ver_alquileres(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Alquileres de Vehículos',
            'res_model': 'javv.alquileres_vehiculos',
            'view_mode': 'tree',
            'domain': [('vehiculo_id.tipo_vehiculo_id', '=', self.id)],
        }

    # Campo para contar alquileres relacionados
    alquileres_count = fields.Integer(string="Alquileres Relacionados", compute="_compute_alquileres_count")

    @api.depends('vehiculos_ids.alquileres_ids')
    def _compute_alquileres_count(self):
        for record in self:
            record.alquileres_count = sum(len(vehiculo.alquileres_ids) for vehiculo in record.vehiculos_ids)

    def action_estadisticas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Alquileres Relacionados',
            'res_model': 'javv.alquileres_vehiculos',
            'view_mode': 'tree,form',
            'domain': [('vehiculo_id.tipo_vehiculo_id', '=', self.id)],
            'context': {'default_tipo_vehiculo_id': self.id},
        }

    kanban_clasificacion_display = fields.Char(
        string="Clasificación para Kanban",
        compute="_compute_kanban_clasificacion_display"
    )

    @api.depends('clasificacion_energetica', 'enganche_carro')
    def _compute_kanban_clasificacion_display(self):
        for record in self:
            display = []
            if record.clasificacion_energetica in ['0', 'eco']:
                display.append(f"Clasificación: {record.clasificacion_energetica}")
            if record.enganche_carro:
                display.append("Enganche para carro disponible")
            record.kanban_clasificacion_display = "\n".join(display)