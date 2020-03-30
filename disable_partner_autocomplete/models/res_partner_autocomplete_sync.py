from odoo import api, models


class ResPartnerAutocompleteSync(models.Model):
    _inherit = "res.partner.autocomplete.sync"

    @api.model
    def start_sync(self):
        pass
