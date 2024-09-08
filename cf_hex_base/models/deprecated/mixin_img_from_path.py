import base64
import logging
from pathlib import Path
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class MixinImgFromPath(models.AbstractModel):
    _name = 'mixin.img.from.path'
    _description = "Mixin to Load Image from Path"

    image_path = fields.Char(
        string="Image URL",
        required=True
    )

    image = fields.Binary(
        string="Image",
        compute="_compute_image",
        attachment=True,
        store=True
    )

    @api.depends("image_path")
    def _compute_image(self):
        for record in self:
            record.image = None  # Reset the image field
            if record.image_path:
                file_path = (Path(__file__).resolve().parents[1] / record.image_path).as_posix()

                # Check if file exists
                if not Path(file_path).is_file():
                    _logger.error(f"Image file not found: {file_path}")
                    raise UserError(_("Image file not found: %s") % record.image_path)

                try:
                    with open(file_path, 'rb') as file:
                        data = base64.b64encode(file.read()).decode('utf-8')
                        if data:
                            record.image = data
                except Exception as e:
                    _logger.error(f"Error reading image file: {file_path}, Error: {e}")
                    raise UserError(_("Error reading image file: %s") % record.image_path)
