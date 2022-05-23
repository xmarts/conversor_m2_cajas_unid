# -*- coding: utf-8 -*-
import logging
import datetime
import traceback
from dateutil.relativedelta import relativedelta
from odoo import fields, api, models, _

from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)

class TecniCeramicaStock(models.Model):
    _inherit = 'product.template'

    unidad = fields.Float(digits=(3,3))
    metros = fields.Float(digits=(3,3))
    cajas = fields.Float(digits=(3,3))



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    unidad = fields.Float(string='Unidad', store=True,digits=(3,3))
    metros = fields.Float(string='Metros',store=True,digits=(3,3))
    cajas = fields.Float(string='Caja', store=True, digits=(3,3))
    #type = ields.selection()
    unidad_x = fields.Float(store=True) #compute='traerDatos' compute='_traer_datos_c',
    metros_x = fields.Float(store=True)
    cajas_x = fields.Float(store=True)

    #@api.depends('unidad_x', 'cajas_x')
#    def _traer_datos(self):
        #for line in self:
            #unidad = line.quantity/line.product_id.cajas*line.product_id.unidad
            #cajas = line.quantity/line.product_id.cajas
                #self.quantity = self.unidad*self.metros_x
            #return self.unidad

                #caja * unidad_x = unidad
                #metros / cajas_X = cajas
    #@api.depends('quantity')
    #def _traer_datos_c(self):
    #    for line in self.move_id:
    #        if line.type == "in_invoice":
    #            for i in self:
    #                if len(i.product_id):
    #                    self.unidad_x = i.product_id.unidad
    #                    self.metros_x = i.product_id.metros
    #                    self.cajas_x = i.product_id.cajas

    #                    self.unidad_c = self.quantity/self.cajas_x*line.unidad_x
    #                    self.cajas_c = self.quantity/self.cajas_x



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    unidad = fields.Float(string='Unidad',default=0.0, store=True, digits=(3,3))
    metros = fields.Float(string='Metros',default=0.0, store=True, digits=(3,3))
    cajas = fields.Float(string='Caja',default=0.0, store=True, digits=(3,3))

    unidad_x = fields.Float(store=True) #compute='traerDatos'
    metros_x = fields.Float(store=True)
    cajas_x = fields.Float(store=True)

    product = fields.Boolean(default=False)

    @api.onchange('product_id', 'cajas', 'product_uom_qty')
    def _traer_datos(self):
        for line in self:
            if line.product_id.type == 'product':
                line.product = True
                line.unidad_x = line.product_id.unidad
                line.metros_x = line.product_id.metros
                line.cajas_x = line.product_id.cajas

                if line.product_id.cajas:
                    line.unidad = round(line.cajas*line.unidad_x)
                    line.cajas = line.product_uom_qty/line.cajas_x
                #self.quantity = self.unidad*self.metros_x
            #return self.unidad

                #caja * unidad_x = unidad
                #metros / cajas_X = cajas


    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({
            #'quantity': self.product_uom_qty,
            'cajas': self.cajas,
            'unidad': self.unidad,

        })
        return res

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    unidad = fields.Float(string='Unidad',default=1.0, store=True, digits=(3,3))
    cajas = fields.Float(string='Caja',default=1.0, store=True, digits=(3,3))

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

    def _prepare_account_move_line(self, move):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        res.update({
        'cajas': self.cajas,
        'unidad': self.unidad,
        })
        return res

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    unidad = fields.Float()
    cajas = fields.Float()

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_infor_stock_move(self):
        lista = []
        for rec in self.move_ids_without_package:
            lista.append({
                "product_id": rec.product_id.id,
                "product_uom_qty": rec.product_uom_qty,
                "reserved_availability": rec.reserved_availability,
                "unidad": rec.unidad,
                "cajas": rec.cajas
            })

        return lista

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('order_line')
    def _check_exist_product_in_line(self):
      for rec in self:
          exist_product_list = []
          for line in rec.order_line:
             if line.product_id.id in exist_product_list:
                raise ValidationError(_('Producto duplicado en las lineas de la orden.'))
             exist_product_list.append(line.product_id.id)

