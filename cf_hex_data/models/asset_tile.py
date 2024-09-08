import base64
import os
from pathlib import Path

from odoo import models, api


class AssetTile(models.Model):
    _inherit = "asset.tile"
    _description = "Asset Tile"

    @api.model
    def load_images(self):
        # Percorso della cartella con le immagini
        file_path = Path(__file__).resolve().parents[1] / 'static/asset/tile'

        # Usa Path.rglob per trovare tutti i file PNG nelle sottocartelle
        for img_path in file_path.rglob('*.png'):
            sub_dir = img_path.relative_to(file_path).parent.as_posix()

            # Apri e codifica l'immagine in base64
            with img_path.open('rb') as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data)

                # Crea un record con l'immagine
                self.create({
                    'name': img_path.name,  # Usa il nome del file come nome del record o personalizza
                    'image': img_base64,
                    'sub_dir': sub_dir,
                })
