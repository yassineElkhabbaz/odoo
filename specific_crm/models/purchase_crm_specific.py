# -*- coding: utf-8 -*-

from odoo import _,fields,models,api
import odoo.addons.decimal_precision as dp


class PurchaseOrderInherit(models.Model):
    _inherit="purchase.order"

    type_achat= fields.Selection([('opportunity', u'Marché'), ('achat', 'Achat'), ('opportunity', 'BC')], u'Type')
    opportunity_id = fields.Many2one('crm.lead', string='Opportunité', domain="[('type', '=', 'opportunity')]")
    delai_livraison = fields.Char(string="Délai de livraison")
    lieu_livraison = fields.Char(string="Lieu de livraison")
    mode_reglement = fields.Char(string="Mode de réglement")

    sale_line_id = fields.Many2one('sale.order', string='SO')

class CrmLeadPurchase(models.Model):
    _inherit = 'crm.lead'

    purchase_amount_total = fields.Monetary(compute='_compute_purchase_amount_total', string="Total des demandes",
                                        help="Untaxed Total of Confirmed Orders", currency_field='company_currency')
    purchase_number = fields.Integer(compute='_compute_purchase_amount_total', string="Nombre de demande produit")
    purchase_ids = fields.One2many('purchase.order', 'opportunity_id', string='Orders')

    @api.depends('purchase_ids')
    def _compute_purchase_amount_total(self):
        for lead in self:
            total = 0.0
            nbr = 0
            company_currency = lead.company_currency or self.env.user.company_id.currency_id
            for order in lead.purchase_ids:
                if order.state in ('draft', 'sent'):
                    nbr += 1
                if order.state not in ('draft', 'sent', 'cancel'):
                    total += order.amount_total

            lead.purchase_amount_total = total
            lead.purchase_number = nbr
