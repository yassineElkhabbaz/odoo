# -*- coding: utf-8 -*-

from odoo import _,fields,models,api


class CrmLead(models.Model):
    _inherit="crm.lead"

    name = fields.Char(
        "Objet de l'AO", index=True, required=True,
        compute='_compute_name', readonly=False, store=True)
    file_offre = fields.Binary("Offre financière")
    #rubrique = fields.Selection([('consulting','Consulting'),('technology','Technology'),('security','et Securtiy Institut')],string="Filiale concernée")
    date_limit = fields.Datetime("Date limite")
    number = fields.Char(u"Numéro",default=lambda self: _('New'), index=True, copy=False)
    # softetude
    num_order= fields.Char(string=u"N° ordre")
    num_reference= fields.Char(string=u"N° référence")
    caution_budget= fields.Char(string=u"Caution/Budget")
    ville_ao = fields.Char(string=u"Ville")
    #date_limite= fields.Datetime(string=u"Date Limite")
    addr_retrait= fields.Text(string=u"Adresse retrait")
    date_ouv_plis= fields.Date(string=u"Date de remise des plis")
    mode_paiement= fields.Char(string=u"Mode paiement")
    data_dep_ech= fields.Date(string=u"Date Dépot D'ech")
    date_reunion= fields.Datetime(string=u"Date réunion")
    delai_execu= fields.Float(string=u"Délai D'exécution")
    montant_retrait= fields.Float(string=u"Montant retrait")
    visite_lieux_date= fields.Datetime(string=u"Visite des lieux")
    type_ao= fields.Char(string=u"Type ao")
    observation= fields.Char(string=u"Obsérvation")
    secteurs= fields.Text(string=u"Secteur(s)")
    partner_id = fields.Many2one('res.partner', string=u"Maître d'ouvrage", track_visibility='onchange', index=True, required=True,
        help="Linked partner (optional). Usually created when converting the lead.")

    montant_avance= fields.Float(string=u"Montant avance")
    is_avance_recup= fields.Boolean(string=u"Avance récupérée ?")
    nbre_provisoire= fields.Float(string=u"Nombre de réception partielle")
    is_reception_def= fields.Boolean(string=u"Réception définitive réalisée ?")
    is_reception_provisoire= fields.Boolean(string=u"Réception provisoire réalisée ?")
    retenu_garanti= fields.Float(string=u"Retenue de garantie")
    is_retenu_recup= fields.Boolean(string=u"Retenue de garantie récupérée ?")
    caution_def= fields.Float(string=u"Caution définitive")
    is_caution_recup= fields.Boolean(string=u"Caution définitive récupérée ?")
    # moyen_materiel_ids = fields.One2many('moyen.materiel', 'crm_id', string=u'Moyens materiels', copy=True)
    # moyen_humain_ids = fields.One2many('moyen.humain', 'crm_id', string=u'Moyens humains', copy=True)

    montant_ht = fields.Float(string=u"Montant hors TVA")
    tax = fields.Float(string=u'Taux TVA (en %)', default=20.0)
    montant_tva = fields.Float(string=u"Montant TVA", compute="_get_montant_total")
    montant_ttc_mad = fields.Float(string=u"Montant TTC en MAD")

    # carriere_prelev_ids = fields.One2many('carriere.prelev.line', 'name', string=u'PRELEVEMENT DE LA CARRIERE', copy=True)

    planned_revenue = fields.Float(string='Budget marché', track_visibility='always')
                                   #, compute="_get_montant_total", store=True)

    doc_attachment_leads = fields.Many2many('ir.attachment', string="Pièces jointes ...")

    # __________
    reference = fields.Char(string="AO N°")
    currency_id = fields.Many2one('res.currency', string='Currency')
    company_currency = fields.Many2one("res.currency", string='Currency', related='company_id.currency_id',
                                       readonly=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    estimation = fields.Monetary('Estimation', currency_field='company_currency', tracking=True)
    # partner_id = fields.Many2one(
    #     'res.partner', string='Le maitre d’ouvrage', index=True, tracking=10,
    #     domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    published_date = fields.Datetime(string="Date de la publication")
    nature = fields.Char(string="Nature de l'AO")
    object = fields.Char(string="Objet")
    address = fields.Char(string="Adresse")
    amount = fields.Monetary('Montant de la caution', currency_field='company_currency', tracking=True)
    qualification = fields.Char(string="Qualification")
    downloaded_date = fields.Datetime(string="Date de téléchargement")
    start_date = fields.Datetime(string="Date de début")
    submission_deadline = fields.Datetime(string="Date limite de soumission")
    judgment_mode = state = fields.Selection(
        [('lot', 'Par lot'), ('article', 'Par article')],
        string='Type de jugement', tracking=True, default='lot')
    nbre_lot=fields.Integer(string=u"Nombre de lot", default=1)
    lot_multiple_ids=fields.One2many('lot.multiple', 'crm_id', string='Lots')
        # fields.Many2one('management.tenders.judgment', string="Mode de jugement")
    user_id = fields.Many2one('res.users', string='Responsable', index=True, tracking=True,
                              default=lambda self: self.env.user)
    source = fields.Many2one('management.tenders.source', string="Source")
    members_lines = fields.One2many('management.tenders.validation', 'members_id', string='Members')
    active = fields.Boolean('Active', default=True)
    # folds_lines = fields.One2many('management.tenders.fold', 'crm_id', string='Pils')

    today = fields.Datetime('Today', required=False, readonly=False, default=lambda self: fields.datetime.now())
    marche_description = fields.Html('Commentaire marché')

    folder_lines = fields.One2many('management.tenders.folder', 'crm_id',string="Dossiers ...")
    # folder_lines = fields.Many2many('ir.attachment', string="Pièces jointes ...")
    delai = fields.Char(string="Délai de livraison")
    adresse_livraison = fields.Char(string="Adresse de livraison")

    state = fields.Selection(
        [('new', 'Nouveau / Téléchargé'), ('qualified', 'Qualifié'), ('preparation', 'En préparation'),
         ('fold', 'Plis déposé'), ('won', 'Gagné'), ('lost', 'Perdu')],
        string='Status', required=True, tracking=True, copy=False, default='new',
        group_expand='_group_expand_states')

    tag_ids = fields.Many2many(
        'crm.tag', 'crm_tag_rel', 'lead_id', 'tag_id', string='State',
        help="Classify and analyze your lead/opportunity categories like: Training, Service")

    marche_type = state = fields.Selection(
        [('cadre', 'Cadre'), ('ferme', 'Ferme')],
        string='Type de marché', tracking=True, default='cadre')

    _sql_constraints = [
        ('number_lead_uniq', 'unique(number)', "Numéro de l'opportunité doit être unique !"),
    ]


    def action_bp_new(self):
        if not self.partner_id:
            return self.env["ir.actions.actions"]._for_xml_id("sale_crm.crm_quotation_partner_action")
        else:
            return self.action_new_quotation()

    # @api.multi
    @api.depends('montant_ht', 'tax')
    def _get_montant_total(self):
        for p in self:
            p.montant_tva = p.montant_ht * p.tax / 100

    # @api.multi
    @api.onchange('montant_ht', 'tax')
    def _get_montant_total_ttc(self):
        for p in self:
            p.montant_tva = p.montant_ht * p.tax / 100
            p.montant_ttc_mad = p.montant_tva + p.montant_ht
            p.planned_revenue = p.montant_tva + p.montant_ht

    # @api.multi
    @api.onchange('planned_revenue', 'tax')
    def _get_montant_total_ht(self):
        for p in self:
            if (1+p.tax/100) :
                p.montant_ht  = p.planned_revenue / (1+p.tax/100)
                p.montant_tva = p.montant_ht * p.tax / 100

    @api.model
    def create(self, vals):
        if vals.get('number', _('New')) == _('New'):
            vals['number'] = self.env['ir.sequence'].next_by_code('crm.lead')
        return  super(CrmLead, self).create(vals)


    @api.depends('order_ids')
    def _compute_sale_amount_total(self):
        for lead in self:
            total = 0.0
            nbr = 0
            company_currency = lead.company_currency or self.env.user.company_id.currency_id
            for order in lead.order_ids:
                # if order.state in ('draft', 'sent', 'sale'):
                #     nbr += 1
                # if order.state not in ('draft', 'sent', 'cancel'):
                total += order.currency_id.compute(order.amount_untaxed, company_currency)
            lead.sale_amount_total = total
            lead.sale_number = nbr

    # @api.multi
    def action_set_qualifie(self):
        """ Won semantic: probability = 30 (active untouched) """
        for lead in self:
            stage_id = lead._stage_find(domain=[('probability', '=', 30.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 30})

    # @api.multi
    def action_set_prop(self):
        """ Won semantic: probability = 70 (active untouched) """
        for lead in self:
            stage_id = lead._stage_find(domain=[('probability', '=', 70.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 70})
