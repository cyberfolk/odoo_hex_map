# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Data",
    'icon': '/cf_hex_base/static/description/cyberfolk.png',
    'sequence': -99,
    'version': '0.0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce i Biomi nella Hex Map",
    'description':
        """In questo modulo vengono salvati i dati per popolare i record.""",
    'license': 'AGPL-3',
    'data': [
        "data/dev_cron.xml",
    ],
    'depends': ['cf_hex_biome'],
    'demo': [],
    'application': False,
    'installable': True,
    'post_init_hook': 'post_init_hook_cf_hex_data',
    'assets': {},
}
