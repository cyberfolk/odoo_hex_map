from odoo import http


class YourController(http.Controller):
    @http.route('/your_controller_route', type='json', auth='public')
    def get_data(self):
        # Your logic here, e.g., returning a dictionary
        data = {"key1": "value1", "key2": "value2"}
        return data
