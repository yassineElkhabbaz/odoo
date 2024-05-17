from odoo import fields, models, api, _
from random import randint
from datetime import datetime

class LotMultipleCRM(models.Model):
    _name = "lot.multiple"
    _inherit = 'mail.thread'

    name = fields.Char(string="Numéro du lot",required=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string='Currency')
    company_currency = fields.Many2one("res.currency", string='Currency', related='company_id.currency_id',
                                       readonly=True)
    caution = fields.Monetary('Caution', currency_field='company_currency', tracking=True)
    estimation = fields.Monetary('Estimation', currency_field='company_currency', tracking=True)
    crm_id= fields.Many2one("crm.lead", string="CRM")

class ManagementTendersSource(models.Model):
    _name = "management.tenders.source"
    _inherit = 'mail.thread'

    name = fields.Char(string="Nom",required=True)
    url = fields.Char(string="Site web")


class ManagementTendersJudgment(models.Model):
    _name = "management.tenders.judgment"
    _inherit = 'mail.thread'

    name = fields.Char(string="Nom",required=True)


class ManagementTendersValidation(models.Model):
    _name = "management.tenders.validation"

    members_id = fields.Many2one('crm.lead', string='Membres', ondelete='cascade', index=True,
                                 copy=False)
    member_id = fields.Many2one('res.users', string='Member', default=lambda self: self.env.user,required=True)
    note = fields.Html(string='Remarque')


class ManagementTendersStage(models.Model):
    _name = "management.tenders.stage"
    _inherit = 'mail.thread'

    name = fields.Char('Nom', required=True)
    sequence = fields.Integer('Sequence', default=10, help="Used to order stages. Lower is better.")

# dossier de soumission
class ManagementTendersDoss(models.Model):
    _name = "management.tenders.dossier"

    name = fields.Char('Nom dossier',required=True)


class ManagementTendersFolder(models.Model):
    _name = "management.tenders.folder"

    name = fields.Many2one('management.tenders.dossier', string='Dossier',required=True)
    doc_attachment = fields.Many2many('ir.attachment', string="Pièces jointes ...")
    crm_id = fields.Many2one('crm.lead', string="Appel d'offre")
