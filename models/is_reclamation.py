# -*- coding: utf-8 -*-

from odoo import api, fields, models
from openerp.exceptions import Warning
import time
from datetime import datetime


#TODO :

# - Revoir le champ 'Pour' de l'envoi d'un mail pour afficher les mails rééls et non pas des liens avec des 
# - Ajouter le client dans les foloower, sinon le client n'est pas destinataire des mails

# - Lors de l'envoi du mail avec le bouton, le champ cc du modèle se retrouve dans le champ 'to' => Remettre en cc
#   Dans le modèle de mail, il est bien possible de mettre une personne en copie, mais ce champ se 
#   retrouve dans les destinataire lors de l'envoi car le model mail.message ne contient pas de champ 'copie'

# - Demander la création du sous domaine odoo.xxxx
# - Demander les mot de passe pour les 2 messageries à intégrer les mails


class IsReclamation(models.Model):
    _name = 'is.reclamation'
    _inherit = ['mail.thread']
    _order = 'num desc'

    num                   = fields.Char('N° de réclamation', readonly=True)


    suivi_par_id          = fields.Many2one('res.users', string='Suivi par')
    mail_template_id = fields.Many2one('mail.template', 
        string='Modèle de courriel associé',
        domain=[('model_id.name','=','is.reclamation')])
    collectivite_id       =  fields.Many2one('res.partner', string='Collectivité', domain=[('is_company','=',True),('customer','=',True)])
    date_creation            = fields.Datetime('Date de création', readonly=True,default=fields.datetime.now())
    ville                 = fields.Char('Ville')
    usager                = fields.Char('Usager')
    adresse               = fields.Text('Adresse')
    objet_id              = fields.Many2one('is.reclamation.objet', string='Objet')
    info                  = fields.Text('Info')
    secteur               = fields.Selection([
        ('bourgogne'    , u'Bourgogne'),
        ('ile_de_france', u'Ile de France'),
    ], 'Secteur')
    date_prise_en_compte  = fields.Datetime('Date de prise en compte', readonly=True)
    observation           = fields.Text('Observation')
    date_cloture          = fields.Datetime('Date de clôture', readonly=True)
    reponse_cloture       = fields.Text('Réponse clôture')
    delai_prise_en_compte = fields.Float('Délai pris en compte (H)', readonly=True, digits=[12,4])
    delai_cloture         = fields.Float('Délai clôture (H)'       , readonly=True, digits=[12,4])
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

        print res.message_follower_ids
        print vals

        return res


    @api.multi
    def prendre_en_compte_action(self):
        for obj in self:
            if obj.observation==False:
                raise Warning(u"Il est obligatoire de renseigner le champ 'Observation'")
            obj.date_prise_en_compte=fields.datetime.now()
            date_creation             = time.mktime(time.strptime(obj.date_creation, '%Y-%m-%d %H:%M:%S'))
            date_prise_en_compte      = time.mktime(time.strptime(obj.date_prise_en_compte, '%Y-%m-%d %H:%M:%S'))
            delai_prise_en_compte     = (date_prise_en_compte - date_creation)/3600

            print delai_prise_en_compte

            obj.delai_prise_en_compte = delai_prise_en_compte
            obj.state="en_attente"


    @api.multi
    def cloturer_action(self):
        for obj in self:
            if obj.reponse_cloture==False:
                raise Warning(u"Il est obligatoire de renseigner le champ 'Réponse clôture'")
            obj.date_cloture=fields.datetime.now()
            date_creation     = time.mktime(time.strptime(obj.date_creation, '%Y-%m-%d %H:%M:%S'))
            date_cloture      = time.mktime(time.strptime(obj.date_cloture, '%Y-%m-%d %H:%M:%S'))
            delai_cloture     = (date_cloture - date_creation)/3600
            obj.delai_cloture = delai_cloture
            obj.state="termine"


    @api.multi
    def send_mail_action(self):
        for obj in self:
            #obj.state="en_attente"

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
            })

#                'default_partner_ids':[13],
#                'default_subject':'toto',
#                'mark_so_as_sent': True,



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






