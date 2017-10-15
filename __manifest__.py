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
],
    'data' : [
        'security/ir.model.access.csv',
        'views/is_reclamation_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [],
}
