# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResPartner(models.Model):
    
    # 1. Private attributes
    _inherit = 'res.partner'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.multi
    def write(self, values):
        user = self.user_id.browse([self._uid]).partner_id

        for field in values:
            field_name = self.fields_get()[field]['string']
            old_value = getattr(self, field)
            new_value = values[field]
            empty_msg = _("(empty)")

            from_value = ''
            to_value = ''

            if isinstance(new_value, dict) or isinstance(new_value, list):
                # Dicts and lists
                from_value = ', '.join([row.display_name for row in old_value])
                new_list = old_value.browse(new_value[0][-1])
                to_value = ', '.join([row.display_name for row in new_list])

            # Booleans
            elif isinstance(new_value, bool):
                booleans = {False: _('No'), True: _('Yes')}
                from_value = booleans[old_value]
                to_value = booleans[new_value]

            elif isinstance(new_value, str) or isinstance(field_name, str) or field_name.isnumeric:
                # String-like fields
                from_value = getattr(self, field) or empty_msg
                to_value = new_value or empty_msg


            msg = '<p>'
            msg += '<b>%s</b> ' % user.name
            msg += _('changed value for')
            msg += ' <b>%s</b>:<br/>' % field_name
            msg += ' <b style="color: #aaa;">%s</b>&#8594;<br/>' % from_value
            msg += ' <b>%s</b> ' % to_value

            self.message_post(msg)

        result = super(ResPartner, self).write(values)

        return result

    # 7. Action methods

    # 8. Business methods
