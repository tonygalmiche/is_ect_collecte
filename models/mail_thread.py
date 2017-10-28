# -*- coding: utf-8 -*-

from odoo import api, fields, models
import re
import html2text




class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'


    @api.model
    def message_new(self, msg_dict, custom_values=None):
        data = {}
        if isinstance(custom_values, dict):
            data = custom_values.copy()
        model = self._context.get('thread_model') or self._name
        RecordModel = self.env[model]
        fields = RecordModel.fields_get()
        name_field = RecordModel._rec_name or 'name'
        if name_field in fields and not data.get('name'):
            data[name_field] = msg_dict.get('subject', '')

        #** Partie modifiée pour récupérer des infos du mail *******************
        if model=='is.reclamation':
            #** Recherche du client à partir de son mail ***********************
            email_from=msg_dict.get('from', '')
            match = re.search(r'[\w\.-]+@[\w\.-]+', email_from)
            email_from=match.group(0)
            partner = self.env['res.partner'].search([('email','=',email_from)])
            if partner.parent_id:
                partner=partner.parent_id
            #*******************************************************************
            server_id=self._context.get('fetchmail_server_id',False)
            server = self.env['fetchmail.server'].browse(server_id)
            info=msg_dict.get('body', '')
            try:
                info=html2text.html2text(info)
            except ValueError:
                pass
            try:
                info=u'Sujet du mail : '+msg_dict.get('subject', '')+'\n\n'+info
            except ValueError:
                pass
            data['email_from']       = msg_dict.get('from', '')
            data['email_to']         = msg_dict.get('to', '')
            data['email_cc']         = msg_dict.get('cc', '')
            data['info']             = info
            data['date_creation']    = msg_dict.get('date', '')
            data['suivi_par_id']     = server.is_user_id.id
            data['mail_template_id'] = server.is_mail_template_id.id
            data['secteur']          = server.is_secteur
            data['collectivite_id']  = partner.id
            data['origine_demande']  = 'mail'
        #***********************************************************************

        res = RecordModel.create(data)
        return res.id

