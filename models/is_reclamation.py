# -*- coding: utf-8 -*-

from odoo import api, fields, models
from openerp.exceptions import Warning
import time
from datetime import datetime


class IsReclamation(models.Model):
    _name = 'is.reclamation'
    _inherit = ['mail.thread','ir.needaction_mixin']
    _order = 'num desc'

    num                   = fields.Char('N° de réclamation', readonly=True)
    suivi_par_id          = fields.Many2one('res.users', string='Suivi par')
    mail_template_id = fields.Many2one('mail.template', 
        string='Modèle de courriel associé',
        domain=[('model_id.name','=','is.reclamation')])
    collectivite_id       =  fields.Many2one('res.partner', string='Collectivité', domain=[('is_company','=',True),('customer','=',True)])
    date_creation         = fields.Datetime('Date de création',default=fields.datetime.now())
    ville                 = fields.Char('Ville')
    usager                = fields.Char('Usager')
    adresse               = fields.Text('Adresse')
    objet_id              = fields.Many2one('is.reclamation.objet', string='Objet')
    info                  = fields.Text('Info')
    secteur               = fields.Selection([
        ('bourgogne'    , u'Bourgogne'),
        ('ile_de_france', u'Ile de France'),
    ], 'Secteur')
    date_prise_en_compte  = fields.Datetime('Date de prise en compte')
    observation           = fields.Text('Observation')
    date_cloture          = fields.Datetime('Date de clôture')
    reponse_cloture       = fields.Text('Réponse clôture')
    delai_prise_en_compte = fields.Float('Délai pris en compte (H)', compute='_compute', store=True, readonly=True, digits=[12,4])
    delai_cloture         = fields.Float('Délai clôture (H)'       , compute='_compute', store=True, readonly=True, digits=[12,4])
    origine_demande       = fields.Selection([
        ('mail'         , u'Mail'),
        ('telephone'    , u'Téléphone'),
        ('site_internet', u'Site internet'),
    ], 'Origine de la demande', required=True, default='telephone')
    name                  = fields.Text('Sujet du mail')
    email_from            = fields.Char('From', readonly=True)
    email_to              = fields.Char('To'  , readonly=True)
    email_cc              = fields.Char('Cc'  , readonly=True)
    state                 = fields.Selection([
        ('a_traiter' , u'A traiter'),
        ('en_attente', u'En attente'),
        ('termine'   , u'Terminée'),
    ], 'Etat', index=True, default='a_traiter', readonly=True)


    @api.depends('date_creation','date_prise_en_compte','date_cloture')
    def _compute(self):
        for obj in self:
            date_creation             = time.mktime(time.strptime(obj.date_creation, '%Y-%m-%d %H:%M:%S'))
            date_prise_en_compte      = time.mktime(time.strptime(obj.date_prise_en_compte, '%Y-%m-%d %H:%M:%S'))
            delai_prise_en_compte     = (date_prise_en_compte - date_creation)/3600
            obj.delai_prise_en_compte = delai_prise_en_compte

            date_creation     = time.mktime(time.strptime(obj.date_creation, '%Y-%m-%d %H:%M:%S'))
            date_cloture      = time.mktime(time.strptime(obj.date_cloture, '%Y-%m-%d %H:%M:%S'))
            delai_cloture     = (date_cloture - date_creation)/3600
            obj.delai_cloture = delai_cloture


    @api.model
    def _needaction_count(self, domain=None):
        if domain==[] or domain==[('state', '=', 'termine')]:
            return False
        ids=self.env['is.reclamation'].search(domain)
        return len(ids)


    @api.multi
    def name_get(self):
        res=[]
        for obj in self:
            name=obj.num
            if obj.objet_id:
                name=name+u' - '+obj.objet_id.name
            res.append((obj.id, name))
        return res


    @api.model
    def create(self, vals):
        sequences = self.env['ir.sequence'].search([('code','=','is.reclamation')])
        for sequence in sequences:
            vals['num'] = sequence.next_by_id()
        res = super(IsReclamation, self).create(vals)
        return res


    @api.multi
    def prendre_en_compte_action(self):
        for obj in self:
            if obj.observation==False:
                raise Warning(u"Il est obligatoire de renseigner le champ 'Observation'")
            obj.date_prise_en_compte=fields.datetime.now()
            obj.state="en_attente"


    @api.multi
    def cloturer_action(self):
        for obj in self:
            if obj.reponse_cloture==False:
                raise Warning(u"Il est obligatoire de renseigner le champ 'Réponse clôture'")
            obj.date_cloture=fields.datetime.now()
            obj.state="termine"


    @api.multi
    def send_mail_action(self):
        for obj in self:
            ir_model_data = self.env['ir.model.data']
            try:
                template_id = ir_model_data.get_object_reference('sale', 'email_template_edi_sale')[1]
            except ValueError:
                template_id = False
            try:
                compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
            except ValueError:
                compose_form_id = False

            template_id=obj.mail_template_id.id
            ctx = dict()
            ctx.update({
                'default_model': 'is.reclamation',
                'default_res_id': self.ids[0],
                'default_composition_mode': 'comment',
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_partner_ids':[(6, 0, [obj.collectivite_id.id])]
            })
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(compose_form_id, 'form')],
                'view_id': compose_form_id,
                'target': 'new',
                'context': ctx,
            }


class IsReclamationObjet(models.Model):
    _name = 'is.reclamation.objet'

    name = fields.Char('Objet de la réclamantion')






