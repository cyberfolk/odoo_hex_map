# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Script",
    'icon': '/cf_hex_base/static/description/cyberfolk.png',
    'sequence': -100,
    'version': '0.0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce gli Hex-Script nella Hex Map",
    'description':
        """In questo modulo vengono introdotti gli Hex-Script, ovvero i modelli che descrivono la lore del singolo
         esagoni, e li collegano ai relativi biomi e alle creature che lo popolano.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/menu_root.xml",
        "views/hex_hex.xml",
        "views/biome_biome.xml",
        "views/hex_script.xml",
    ],
    'depends': ['cf_hex_base', 'cf_hex_biome'],
    'demo': [],
    'application': False,
    'installable': True,
}
