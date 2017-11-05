# -*- coding: utf-8 -*-
import base64
import re
from odoo import _, api, fields, models, SUPERUSER_ID, tools
from odoo.tools.safe_eval import safe_eval


class MailComposer(models.TransientModel):
    _name = 'mail.compose.message'
    _inherit = 'mail.compose.message'


    @api.model
    def default_get(self, fields):
        res = super(MailComposer, self).default_get(fields)
        #res['partner_ids']=[(6, 0, [10,1300])]
        #res['subject']='toto et tutu'
        #res['email_to']='tony.galmiche.to@free.fr'
        return res


