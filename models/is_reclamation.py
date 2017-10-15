# -*- coding: utf-8 -*-

from odoo import api, fields, models
import time

#TODO : 
# - Liste de choix pour 'objet_id'
# - Récupérer les champs to et cc des mails
# - Voir pour mettre le contenu du mail dans le champ 'name' en plus du sujet (champs cachés ?)
# - Créer les boutons pour répondre à la demande et solder la demande
# - Ajouter menu pour récupérer les mails imédiatement
# - Ajouter menu pour gérer les modèles des mails
# - Calcul les champs delai_prise_en_compte et delai_cloture
# - Ajouter une vue graphique et une vue tableau croisé


class IsReclamation(models.Model):
    _name = 'is.reclamation'
    _inherit = ['mail.thread']
    _order = 'name desc'

    num                   = fields.Char('N° de réclamation', readonly=True)
    collectivite_id       = fields.Char('Collectivité')
    date_heure            = fields.Datetime('Date heure')
    ville                 = fields.Char('Ville')
    usager                = fields.Char('Usager')
    adresse               = fields.Text('Adresse')
    objet_id              = fields.Char('Objet')
    name                  = fields.Text('Info')
    secteur               = fields.Char('Secteur')
    heure_prise_en_compte = fields.Datetime('Date et heure prise en compte')
    observation           = fields.Text('Observation')
    date_cloture          = fields.Datetime('Date de clôture')
    reponse_cloture       = fields.Text('Réponse clôture')
    delai_prise_en_compte = fields.Char('Délai pris en compte')
    delai_cloture         = fields.Char('Délai clôture')
    origine_demande_id    = fields.Char('Origine de la demande')
    state                 = fields.Selection([
        ('a_traiter' , u'A traiter'),
        ('en_attente', u'En attente'),
        ('termine'   , u'Terminée'),
    ], 'Etat', index=True, default='a_traiter', readonly=True)


    @api.model
    def create(self, vals):
        data_obj = self.env['ir.model.data']
        sequence_ids = data_obj.search([('name','=','is_reclamation_seq')])
        if sequence_ids:
            sequence_id = data_obj.browse(sequence_ids[0].id).res_id
            vals['num'] = self.env['ir.sequence'].get_id(sequence_id, 'id')
        res = super(IsReclamation, self).create(vals)
        return res

