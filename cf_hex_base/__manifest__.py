# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Base",
    'icon': '/cf_hex_base/static/description/icon.png',
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
        "views/filter_apps.xml",
        "views/asset_tile.xml",
        "data/hex.xml",
    ],
    'depends': ['base', 'web'],
    'demo': [],
    'application': True,
    'installable': True,
    'post_init_hook': 'post_init_hook_cf_hex_base',
    'assets': {
        'web.assets_backend': [
            '/cf_hex_base/static/src/utility/utils.js',
            '/cf_hex_base/static/src/store.js',
            '/cf_hex_base/static/src/scss/style.scss',
            '/cf_hex_base/static/src/widget_quad/*',
            '/cf_hex_base/static/src/ViewMacro/ViewMacro.js',
            '/cf_hex_base/static/src/ViewMacro/ViewMacro.xml',
            '/cf_hex_base/static/src/ViewMacro/CurrentColor/*',
            '/cf_hex_base/static/src/ViewMacro/CurrentZoom/*',
            '/cf_hex_base/static/src/ViewMacro/CurrentTiles/*',
            '/cf_hex_base/static/src/ViewMacro/ClearCurrent/*',
            '/cf_hex_base/static/src/ViewMacro/DirTiles/*',
            '/cf_hex_base/static/src/ViewMacro/HexHex/*',
        ],
        'web.assets_frontend': [
            '/cf_hex_base/static/src/scss/style.scss',
        ]
    },
}
