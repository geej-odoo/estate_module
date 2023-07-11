{
    'name': "Real Estate Module",
    'version': '1.0',
    'category': 'Real Estate/Real Estate',
    'category': 'Real Estate/Brokerage',
    'depends': ['base','mail','website'],
    'data': [
        
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/estate_wizard_views.xml',
        'views/estate_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_properties.xml',
        'views/res_user_views.xml',
        'views/estate_menus.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
        'controllers/templates.xml',
        # 'report/estate_account_templates.xml',
       
                ],
    'demo': [
        "demo/demo_data.xml",
    ],
    'application': True,
    
}