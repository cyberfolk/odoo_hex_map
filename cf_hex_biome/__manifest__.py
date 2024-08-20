# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Biome",
    'icon': '/cf_hex_base/static/description/cyberfolk.png',
    'sequence': -99,
    'version': '0.0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce i Biomi nella Hex Map",
    'description':
        """In questo modulo vengono introdotti i Biomi nella Hex Map.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/menu_root.xml",
        "views/biome_type.xml",
        "views/structure_structure.xml",
        "views/creature_creature.xml",
        "views/creature_type.xml",
        "views/creature_tag.xml",
        "data/dev_cron.xml",
    ],
    'depends': ['cf_hex_base', 'base', 'web'],
    'demo': [],
    'application': False,
    'installable': True,
    'post_init_hook': 'post_init_hook_cf_hex_biome',
    'assets': {
        'web.assets_backend': [
            '/cf_hex_biome/static/src/css/style.css',
            '/cf_hex_biome/static/src/js/many2many_tags_fields.js',
        ],
        'web.assets_frontend': [
            '/cf_hex_biome/static/src/css/style.css',
        ]
    },
}


