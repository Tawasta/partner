from odoo import api, fields, models


class ResPartnerAutocompleteSync(models.Model):
    _inherit = "res.partner.autocomplete.sync"

    synched = fields.Boolean("Is synched", default=True)

    @api.model
    def dont_sync(self):
        pass
