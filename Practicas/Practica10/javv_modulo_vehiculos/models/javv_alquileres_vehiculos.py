from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta, date
import logging
_logger = logging.getLogger(__name__)

class javv_alquileres_vehiculos(models.Model):
    _name = 'javv.alquileres_vehiculos'
    _description = 'Alquileres de Vehículos'
    _order = "state desc"

    # Campos básicos
    fecha_inicio = fields.Date(string="Fecha de Inicio", required=True, default=fields.Date.today)
    fecha_fin = fields.Date(string="Fecha de Fin")
    precio_final = fields.Float(string="Precio Final", compute="_compute_precio_final", store=True)
    state = fields.Selection([
        ('previo', 'Previo'),
        ('en_proceso', 'En Proceso'),
        ('terminado', 'Terminado'),
        ('facturado', 'Facturado'),
        ('cancelado', 'Cancelado')
    ], string="Estado", default='previo', required=True)


    decoration_state = fields.Char(compute="_compute_decoration_state", string="Decoration State")

    @api.depends('state')
    def _compute_decoration_state(self):
        for record in self:
            if record.state == 'previo':
                record.decoration_state = 'marron_claro'
            elif record.state in ['en_proceso', 'terminado']:
                record.decoration_state = 'verde'
            elif record.state == 'facturado':
                record.decoration_state = 'purpura'
            elif record.state == 'cancelado':
                record.decoration_state = 'rojo'
            else:
                record.decoration_state = False
    # Relaciones
    vehiculo_id = fields.Many2one('javv.vehiculos', string="Vehículo", required=True)
    usuario_id = fields.Many2one('res.users', string="Usuario que gestiona", default=lambda self: self.env.user)
    cliente_id = fields.Many2one('res.partner', string="Cliente", required=True)
    duracion = fields.Integer(string="Duración (días)", compute="_compute_duracion", inverse="_inverse_duracion", store=True)

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                record.duracion = (record.fecha_fin - record.fecha_inicio).days
            else:
                record.duracion = 0

    @api.constrains('fecha_inicio', 'fecha_fin', 'vehiculo_id', 'cliente_id', 'usuario_id', 'state', 'duracion')
    def _check_validaciones(self):
        for record in self:
            # Validación 1: Las fechas son obligatorias y consistentes
            if not record.fecha_inicio or not record.fecha_fin:
                raise ValidationError('Debe proporcionar tanto la fecha de inicio como la fecha de fin.')

            if record.fecha_fin <= record.fecha_inicio:
                raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')

            # Validación 2: Vehículo debe estar disponible
            if record.state == 'previo' and record.vehiculo_id.state != 'disponible':
                raise ValidationError(f'El vehículo "{record.vehiculo_id.name}" no está disponible para alquilar.')

            # Validación 3: Campos obligatorios
            if not all([record.vehiculo_id, record.cliente_id, record.usuario_id]):
                raise ValidationError('Debe completar todos los campos obligatorios: vehículo, cliente y usuario.')

            # Validación 4: No debe haber conflictos con otros alquileres del mismo vehículo
            conflictos = self.env['javv.alquileres_vehiculos'].search([
                ('vehiculo_id', '=', record.vehiculo_id.id),
                ('id', '!=', record.id),  # Excluir el registro actual
                ('state', 'not in', ['cancelado']),  # Excluir alquileres cancelados
                ('fecha_inicio', '<=', record.fecha_fin),
                ('fecha_fin', '>=', record.fecha_inicio)
            ])
            if conflictos:
                raise ValidationError(
                    f'El vehículo "{record.vehiculo_id.name}" ya está alquilado en las fechas seleccionadas.')

            # Validación 5: Si se guarda el alquiler, el vehículo pasa a "alquilado" automáticamente
            if record.state == 'en_proceso':
                record.vehiculo_id.state = 'alquilado'

            # Validación 6: Duración debe ser consistente
            calculada = (record.fecha_fin - record.fecha_inicio).days
            if record.duracion != calculada:
                raise ValidationError('La duración del alquiler no coincide con las fechas de inicio y fin.')


    @api.constrains('vehiculo_id', 'state')
    def _check_estado_vehiculo(self):
        for record in self:
            # No validar si el estado del alquiler es "en_proceso" y va a cambiar a "terminado"
            if record.state == 'en_proceso':
                continue

            if record.vehiculo_id and record.state not in ['cancelado', 'facturado', 'terminado']:
                if record.vehiculo_id.state != 'disponible':
                    raise ValidationError(f'El vehículo "{record.vehiculo_id.name}" no está disponible para alquilar.')

            # Si el estado es "en_proceso", cambiar el estado del vehículo a "alquilado"
            if record.state == 'en_proceso':
                record.vehiculo_id.state = 'alquilado'

    @api.constrains('fecha_inicio', 'fecha_fin', 'duracion')
    def _check_duracion_consistente(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                calculada = (record.fecha_fin - record.fecha_inicio).days
                if record.duracion != calculada:
                    raise ValidationError('La duración del alquiler no coincide con las fechas de inicio y fin.')


    def _inverse_duracion(self):
        for record in self:
            if record.fecha_inicio and record.duracion > 0:
                record.fecha_fin = record.fecha_inicio + timedelta(days=record.duracion)
            else:
                record.fecha_fin = False

    def action_comprobar_alquileres(self):
        for record in self:
            if record.state in ['facturado', 'cancelado']:
                continue  # No cambiar estado si está facturado o cancelado
            hoy = date.today()
            if hoy < record.fecha_inicio:
                record.state = 'previo'
            elif record.fecha_inicio <= hoy <= record.fecha_fin:
                record.state = 'en_proceso'
                if record.vehiculo_id.state == 'disponible':
                    record.vehiculo_id.state = 'alquilado'  # Cambiar estado del vehículo
            elif hoy > record.fecha_fin:
                record.state = 'terminado'
                record.vehiculo_id.state = 'disponible'

    def action_comprobar_estado_individual(self):
        for record in self:
            if record.state in ['facturado', 'cancelado']:
                continue  # No cambiar estado si está facturado o cancelado
            hoy = date.today()
            if hoy < record.fecha_inicio:
                record.state = 'previo'
            elif record.fecha_inicio <= hoy <= record.fecha_fin:
                record.state = 'en_proceso'
            elif hoy > record.fecha_fin:
                record.state = 'terminado'

    # Relación con facturas
    factura_id = fields.Many2one(
        'account.move',
        string="Factura Generada",
        readonly=True,
        help="Factura asociada al alquiler."
    )

    def open_factura(self):
        """
        Botón que abre la factura asociada o lanza una notificación si no existe.
        """
        for record in self:
            if record.factura_id:
                # Redirigir a la factura asociada
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Factura',
                    'res_model': 'account.move',
                    'view_mode': 'form',
                    'res_id': record.factura_id.id,
                    'target': 'current',
                }
            else:
                # Lanzar error si no hay factura asociada
                raise UserError('No existe ninguna factura asociada a este alquiler.')

    # Botón "Facturar alquiler"
    def action_facturar_alquiler(self):
        for record in self:
            # Validar que el alquiler esté en estado "terminado"
            if record.state != 'terminado':
                raise ValidationError(
                    f'El alquiler debe estar en estado "Terminado" para facturarlo. Estado actual: {record.state}.'
                )

            # Crear la factura en el modelo account.move
            factura = self.env['account.move'].create({
                'move_type': 'out_invoice',  # Factura de cliente
                'partner_id': record.cliente_id.id,  # Cliente asociado al alquiler
                'invoice_date': fields.Date.today(),  # Fecha actual
                'journal_id': 1,  # Diario de ventas (asegúrate de que este ID sea válido)
                'invoice_line_ids': [
                    # Primera línea: Detalles del vehículo
                    (0, 0, {
                        'name': f'{record.vehiculo_id.name} ({record.vehiculo_id.codigo}) - {record.duracion} días',
                        'quantity': 1,
                        'price_unit': record.precio_final,  # Precio total del alquiler
                    }),
                    # Segunda línea: Gastos de seguro obligatorio
                    (0, 0, {
                        'name': 'Gastos del seguro obligatorio',
                        'quantity': 1,
                        'price_unit': 20.0,  # Precio fijo del seguro
                    }),
                ]
            })

            # Publicar la factura
            factura.action_post()

            # Relacionar la factura con el alquiler
            record.factura_id = factura.id

            # Cambiar el estado del alquiler a "facturado"
            record.state = 'facturado'

    # Botón "Terminar alquiler"
    def action_terminar_alquiler(self):
        for record in self:
            # Validar el estado actual
            if record.state == 'previo':
                raise ValidationError('El alquiler aún no ha comenzado, no se puede facturar.')
            elif record.state == 'en_proceso':
                raise ValidationError('El alquiler está en curso, no se puede facturar.')
            elif record.state == 'cancelado':
                raise ValidationError('El alquiler está cancelado, no se puede facturar.')

            # Calcular la duración si aún no está definida
            if not record.duracion:
                record.duracion = (record.fecha_fin - record.fecha_inicio).days

            # Calcular el precio final
            if not record.precio_final:
                record._compute_precio_final()

            # Verificar valores críticos antes de continuar
            if record.duracion <= 0:
                raise ValidationError('La duración del alquiler no es válida.')
            if record.precio_final <= 0:
                raise ValidationError('El precio final no se ha calculado correctamente.')

            # Cambiar el estado del alquiler
            record.state = 'terminado'

            # Cambiar el estado del vehículo a "Disponible"
            record.vehiculo_id.state = 'disponible'

    # Botón "Cancelar alquiler"
    def action_cancelar_alquiler(self):
        for record in self:
            if record.state not in ['previo', 'en_proceso']:
                raise ValidationError(
                    f'Solo se pueden cancelar alquileres en estado "Previo" o "En Proceso". Estado actual: {record.state}.')
            record.state = 'cancelado'
            record.vehiculo_id.state = 'disponible'

    # Cálculo del precio final
    @api.depends('duracion', 'vehiculo_id')
    def _compute_precio_final(self):
        for record in self:
            if record.duracion > 0 and record.vehiculo_id:
                precio_diario = record.vehiculo_id.precio_diario or 0
                precio_semanal = record.vehiculo_id.precio_semanal or 0

                semanas = record.duracion // 7
                dias_restantes = record.duracion % 7
                record.precio_final = (semanas * precio_semanal) + (dias_restantes * precio_diario)

                _logger.info(f"Precio Final Calculado: {record.precio_final}")
            else:
                record.precio_final = 0
                _logger.warning(f"Precio Final no calculado correctamente para el alquiler {record.id}")

    # Validación de vehículo disponible
    @api.constrains('vehiculo_id', 'state')
    def _check_vehiculo_disponible(self):
        for record in self:
            if record.state == 'previo' and record.vehiculo_id.state != 'disponible':
                raise ValidationError(f'El vehículo "{record.vehiculo_id.name}" no está disponible para alquilar.')


    # Para que se actualice el campo num_alquileres cada vez que:
        # Se crea un nuevo alquiler asociado al vehículo.
        # Se cancela un alquiler existente.
    @api.model
    def create(self, vals):
        record = super(javv_alquileres_vehiculos, self).create(vals)
        if record.state == 'en_proceso' and record.vehiculo_id.state == 'disponible':
            record.vehiculo_id.state = 'alquilado'
        record.vehiculo_id.numero_alquileres += 1
        return record

    def write(self, vals):
        for record in self:
            if 'state' in vals:
                if vals['state'] == 'cancelado':
                    record.vehiculo_id.numero_alquileres -= 1
                    record.vehiculo_id.state = 'disponible'
                elif vals['state'] == 'en_proceso' and record.vehiculo_id.state == 'disponible':
                    record.vehiculo_id.state = 'alquilado'
        return super(javv_alquileres_vehiculos, self).write(vals)
