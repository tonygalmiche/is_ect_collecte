# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class FetchmailServer(models.Model):
    _inherit = 'fetchmail.server'

    is_user_id          = fields.Many2one('res.users'    , string='Utilisateur associé')
    is_mail_template_id = fields.Many2one('mail.template', 
        string='Modèle de courriel associé',
        domain=[('model_id.name','=','is.reclamation')])

    is_secteur = fields.Selection([
        ('bourgogne'    , u'Bourgogne'),
        ('ile_de_france', u'Ile de France'),
    ], 'Secteur')


