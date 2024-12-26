from odoo import fields, models, Command
from datetime import datetime

class JavvInheritedInmuebles(models.Model):
    _inherit = "javv.propiedades_inmuebles"  # Extiende la clase de propiedades inmobiliarias

    def action_vender_propiedad(self):
        for record in self:
            # Crear una factura en el módulo 'account'
            self.env["account.move"].create({
                'partner_id': record.cliente_id.id,
                'move_type': 'out_invoice',
                'journal_id': 1,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [
                    Command.create({
                        'name': "6% del precio de venta: " + str(record.name),
                        'quantity': 1,
                        'price_unit': record.precio_venta * 0.06,
                    }),
                    Command.create({
                        'name': "Gastos de gestión (" + str(record.name) + ")",
                        'quantity': 1,
                        'price_unit': 100,
                    }),
                ],
            })
        # Llamar al método original de la clase padre
        return super().action_vender_propiedad()
