# -*- coding: utf-8 -*-
from odoo import models, fields


class account_invoice(models.Model):

    _inherit = "account.invoice"

    # Pull name extension suggestion from partner info
    name_extension = fields.Char('Name extension', size=128)

    def onchange_partner_id(self, type, partner_id,\
            date_invoice=False, payment_term=False,
            partner_bank_id=False, company_id=False):

        res = super(account_invoice, self).onchange_partner_id(type, partner_id, \
            date_invoice, payment_term, partner_bank_id, company_id)

        # Only do this for customer invoices, not supplier invoices
        if type == 'out_invoice':

            partner_model = self.env['res.partner']

            # Check if the partner has a name extension defined
            active_partner = partner_model.browse([partner_id])[0]

            res['value']['name_extension'] = active_partner.name_extension

        return res
