# -*- coding: utf-8 -*-

from odoo import fields, api, models
import odoo.addons.decimal_precision as dp


class ResCompanyInh(models.Model):
    _inherit = 'res.company'

    ice = fields.Char(string="ICE")
    tp = fields.Char(string="TP")
    cnss = fields.Char(string="CNSS")
    fax = fields.Char(string="FAX")


