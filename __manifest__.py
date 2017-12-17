# -*- coding: utf-8 -*-
{
    'name'     : 'InfoSaône - Module Odoo ECT Collecte',
    'version'  : '0.1',
    'author'   : 'InfoSaône',
    'category' : 'InfoSaône',


    'description': """
InfoSaône - Module Odoo ECT Collecte
===================================================
""",
    'maintainer' : 'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
        'sale',
        'crm',
        'mail',
        'account',
        'account_accountant',
        'purchase',
        'board',
        'calendar',
        'document',
],
    'data' : [
        'security/res.groups.xml',
        'security/res.groups.csv',
        'security/ir.model.access.csv',
        'security/ir.model.access.xml',
        'views/fetchmail_views.xml',
        'views/mail_message_views.xml',
        'views/is_reclamation_view.xml',
        'views/res_partner_view.xml',
        'views/menu.xml',
        'views/webclient_templates.xml',
        'wizard/mail_compose_message_view.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
    ],
}

