from odoo import models, fields
from odoo.exceptions import ValidationError
from datetime import date

class AlquileresFacturacion(models.Model):
    _inherit = 'javv.alquileres_vehiculos'

    def action_facturar_alquiler(self):
        super(AlquileresFacturacion, self).action_facturar_alquiler()

        for record in self:
            if record.state != 'facturado':
                raise ValidationError('El alquiler debe estar en estado "Terminado" para facturarlo.')

            # Crear la factura
            factura_vals = {
                'partner_id': record.cliente_id.id,
                'move_type': 'out_invoice',
                'journal_id': 1,  # Diario de facturación
                'invoice_date': date.today(),
                'invoice_line_ids': [
                    # Primera línea: información del vehículo
                    (0, 0, {
                        'name': f'{record.vehiculo_id.name} ({record.vehiculo_id.codigo}) - {record.duracion} días',
                        'quantity': 1,
                        'price_unit': record.precio_final,
                    }),
                    # Segunda línea: gastos del seguro obligatorio
                    (0, 0, {
                        'name': 'Gastos del seguro obligatorio',
                        'quantity': 1,
                        'price_unit': 20.0,
                    }),
                ],
            }

            # Crear la factura en el modelo 'account.move'
            factura = self.env['account.move'].create(factura_vals)

            # Registrar la factura
            factura.action_post()

        return True
