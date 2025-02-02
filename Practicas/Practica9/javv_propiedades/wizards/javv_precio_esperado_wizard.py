from odoo import api, fields, models

class javv_precio_esperado_wizard(models.TransientModel):
    _name = "javv.precio_esperado_wizard"
    _description = "Asistente para establecer el precio esperado"

    precio_base = fields.Float(string="Precio Base")
    buena_ubicacion = fields.Boolean(string="Buena Ubicación")
    muy_nuevo = fields.Boolean(string="Muy Nuevo")
    cocina_amueblada = fields.Boolean(string="Cocina Amueblada")

    def establecer_precio_esperado(self):
        """Calcula el precio en función de lo marcado en el wizard y
        lo asigna al inmueble activo."""
        precio = self.precio_base
        if self.buena_ubicacion:
            precio += self.precio_base * 15 / 100
        if self.muy_nuevo:
            precio += self.precio_base * 10 / 100
        if self.cocina_amueblada:
            precio += self.precio_base * 5 / 100


        inmueble = self.env["javv.propiedades_inmuebles"].browse(
            self.env.context.get("active_ids")
        )
        inmueble.precio_esperado = precio

        return {'type': 'ir.actions.act_window_close'}
