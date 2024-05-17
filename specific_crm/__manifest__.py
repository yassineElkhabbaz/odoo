# -*- coding: utf-8 -*-
{
    'name': 'CRM',
    'version': '1.1',
    'category': '',
    'sequence': 35,
    'description': """

""",
    'author': '',
    'depends': ['crm','sale_crm','purchase', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'report/purchase_layout.xml',
        'report/sale_layout.xml',
        'report/sale_tenders_report.xml',
        'report/sale_tenders_templates.xml',
        'report/concis_purchase_order.xml',
        'views/menu_crm.xml',
        'views/lead_view.xml',
        'views/sale_crm_specific.xml',
        'views/res_company_view.xml',
        'views/purchase_crm_view.xml',

    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
