# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP


class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    @api.multi
    def _compute(self):
        for obj in self:
            reclamations = self.env['is.reclamation'].search([('collectivite_id','=',obj.id)])
            obj.is_reclamation_count=len(reclamations)

    is_reclamation_count = fields.Integer(compute='_compute', string=u'Réclamations')


    @api.multi
    def reclamation_action(self):
        for obj in self:
            return {
                'name'     : 'Réclamations',
                'type'     : 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'is.reclamation',
                'domain'   : [('collectivite_id','=',obj.id)],
            }


