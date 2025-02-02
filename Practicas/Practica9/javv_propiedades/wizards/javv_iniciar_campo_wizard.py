from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class javv_iniciar_campo_wizard(models.TransientModel):
    _name = "javv.iniciar_campo_wizard"
    _description = "Asistente para iniciar el campo indicado en todos los registros vacíos"

    campo = fields.Selection([
        ('tipos_id', 'Tipo de inmueble'),
        ('codigo_postal', 'Código Postal'),
        ('dormitorios', 'Nº de Dormitorios'),
    ], string="Nombre del campo", default='tipos_id')

    valor = fields.Char(string="Valor por defecto")

    def iniciar_valor_campo(self):
        """
        Recorre todos los inmuebles que NO estén cancelados,
        y si el campo seleccionado está vacío, se rellena con 'valor'.
        Si el campo es 'tipos_id', se busca un Tipo de Inmueble con `name ilike valor`.
        """
        dominio = [('state', '!=', 'cancelado')]
        inmuebles = self.env["javv.propiedades_inmuebles"].search(dominio)


        for rec in inmuebles:
            dato_campo = rec[self.campo]
            if not dato_campo:
                if self.campo == 'tipos_id':

                    tipo_record = self.env["javv.tipos_inmuebles"].search([('name', 'ilike', self.valor)], limit=1)
                    if tipo_record:
                        rec.tipos_id = tipo_record.id
                elif self.campo == 'codigo_postal':
                    rec.codigo_postal = self.valor
                elif self.campo == 'dormitorios':
                    try:
                        num_dorm = int(self.valor)
                    except ValueError:
                        num_dorm = 0
                    rec.dormitorios = num_dorm

        return {'type': 'ir.actions.act_window_close'}
