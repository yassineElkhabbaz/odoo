# -*- coding: utf-8 -*-

from odoo import _,fields,models,api
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, AccessError

from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit="sale.order"


    state = fields.Selection([
        ('draft', u'BP/SD/Devis'),
        ('sent', 'Document envoyé'),
        ('sale', 'BP/BC validé'),
        ('done', 'Confirmé'),
        ('cancel', 'Annulé'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    b_prix= fields.Boolean('Bordereau des prix ?', default=False, copy=True)

class SaleOrderLine(models.Model):
    _inherit="sale.order.line"

    numero_prix = fields.Char(string="N° Prix",store=True)
    designation = fields.Char(string="Désignation",store=True)

