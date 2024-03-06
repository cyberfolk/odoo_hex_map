# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Map",
    'icon': '/cf_hex_map/static/description/icon.png',
    'sequence': -100,
    'version': '0.0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce gli elementi base della Hex Map",
    'description':
        """In questa app vengono introdotti gli elementi base della Hex Map: ovvero Macro-area, Quadranti ed Esagoni.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/menu_root.xml",
        "views/hex_hex.xml",
        "views/hex_quad.xml",
        "data/data.xml",
    ],
    'depends': ['base', 'web'],
    'demo': [],
    'application': True,
    'installable': True,
    'post_init_hook': 'post_init_hook_hex_map',
    'assets': {
        'web.assets_backend': [
            '/cf_hex_map/static/src/scss/style.scss',
            '/cf_hex_map/static/src/widget_quad/*',
            '/cf_hex_map/static/src/view_macro/*',
        ],
        'web.assets_frontend': [
            '/cf_hex_map/static/src/scss/style.scss',
        ]
    },
}
