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
        "views/hex_macro.xml",
        "views/hex_quad.xml",
        "data/data.xml",
    ],
    'depends': [],
    'demo': [],
    'application': True,
    'installable': True,
    'assets': {},
}


