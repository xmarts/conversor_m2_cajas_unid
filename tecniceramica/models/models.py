# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

class TecniCeramicaStock(models.Model):
    _inherit = 'product.template'

    unidad = fields.Float(digits=(12,6))
    metros = fields.Float(digits=(12,6))
    cajas = fields.Float(digits=(12,6))



class TecniCeramicaLine(models.Model):
    _inherit = 'account.move.line'

    unidad = fields.Float(string='Unidad',default=1.0, store=True, digits=(12,6))
    metros = fields.Float(string='Metros',default=1.0, store=True, digits=(12,6))
    cajas = fields.Float(string='Caja',default=1.0, store=True, digits=(12,6))

    unidad_x = fields.Float(store=True) #compute='traerDatos'
    metros_x = fields.Float(store=True)
    cajas_x = fields.Float(store=True)

    @api.onchange('product_id', 'cajas', 'quantity')
    def _traer_datos(self):
        for line in self:
            if self.product_id:
                self.unidad_x = line.product_id.unidad
                self.metros_x = line.product_id.metros
                self.cajas_x = line.product_id.cajas

                self.unidad = self.cajas*self.unidad_x
                self.cajas = self.quantity/self.cajas_x
                #self.quantity = self.unidad*self.metros_x
            #return self.unidad

                #caja * unidad_x = unidad
                #metros / cajas_X = cajas


class TecniCeramicaLine(models.Model):
    _inherit = 'sale.order.line'

    unidad = fields.Float(string='Unidad',default=1.0, store=True, digits=(12,6))
    metros = fields.Float(string='Metros',default=1.0, store=True, digits=(12,6))
    cajas = fields.Float(string='Caja',default=1.0, store=True, digits=(12,6))

    unidad_x = fields.Float(store=True) #compute='traerDatos'
    metros_x = fields.Float(store=True)
    cajas_x = fields.Float(store=True)

    @api.onchange('product_id', 'cajas', 'product_uom_qty')
    def _traer_datos(self):
        for line in self:
            if self.product_id:
                self.unidad_x = line.product_id.unidad
                self.metros_x = line.product_id.metros
                self.cajas_x = line.product_id.cajas

                self.unidad = self.cajas*self.unidad_x
                self.cajas = self.product_uom_qty/self.cajas_x
                #self.quantity = self.unidad*self.metros_x
            #return self.unidad

                #caja * unidad_x = unidad
                #metros / cajas_X = cajas


class TecniCeramicaLine(models.Model):
    _inherit = 'purchase.order.line'

    unidad = fields.Float(string='Unidad',default=1.0, store=True, digits=(12,6))
    metros = fields.Float(string='Metros',default=1.0, store=True, digits=(12,6))
    cajas = fields.Float(string='Caja',default=1.0, store=True, digits=(12,6))

    unidad_x = fields.Float(store=True) #compute='traerDatos'
    metros_x = fields.Float(store=True)
    cajas_x = fields.Float(store=True)

    @api.onchange('product_id', 'cajas', 'product_qty')
    def _traer_datos(self):
        for line in self:
            if self.product_id:
                self.unidad_x = line.product_id.unidad
                self.metros_x = line.product_id.metros
                self.cajas_x = line.product_id.cajas

                self.unidad = self.cajas*self.unidad_x
                self.cajas = self.product_qty/self.cajas_x
                #self.quantity = self.unidad*self.metros_x
            #return self.unidad

                #caja * unidad_x = unidad
                #metros / cajas_X = cajas
