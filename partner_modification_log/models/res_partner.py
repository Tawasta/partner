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

        for record in self:
            user = record.user_id.browse([self._uid]).partner_id

            for field in values:
                this_field = record.fields_get()[field]
                field_name = this_field['string']
                field_type = this_field['type']

                old_value = getattr(record, field)
                new_value = values[field]

                from_value = ''
                to_value = ''

                if field_type == 'many2many':
                    # Dicts and lists
                    from_value = ', '.join([row.display_name for row in old_value])
                    new_list = old_value.browse(new_value[0][-1])
                    to_value = ', '.join([row.display_name for row in new_list])

                elif field_type == 'boolean':
                    # Booleans
                    booleans = {False: _('No'), True: _('Yes')}
                    from_value = booleans[old_value]
                    to_value = booleans[new_value]

                elif field_type in ('char', 'text', 'html', 'integer', 'float'):
                    # String-like fields
                    from_value = getattr(record, field)
                    to_value = new_value

                elif field_type == 'selection':
                    # Selection fields
                    from_value = False
                    to_value = False

                    if old_value:
                        from_value = dict(this_field['selection'])[old_value]
                    if new_value:
                        to_value = dict(this_field['selection'])[new_value]

                elif field_type == 'many2one':
                    # Many2one
                    from_value = old_value.display_name
                    to_value = old_value.browse([new_value]).display_name

                elif field_type == 'one2many':
                    # One2many
                    from_value = ', '.join([row.display_name for row in old_value])
                    to_value = _('(See "%s")') % field_name

                # Prevent Odoo from printing "False"
                empty_msg = _("(empty)")
                from_value = from_value or empty_msg
                to_value = to_value or empty_msg

                msg = '<p>'
                msg += '<b>%s</b> ' % user.name
                msg += _('changed value for')
                msg += ' <b>%s</b>:<br/>' % field_name
                msg += ' <b style="color: #aaa;">%s</b>&#8594;<br/>' % from_value
                msg += ' <b>%s</b> ' % to_value

                record.message_post(body=msg)

        result = super(ResPartner, self).write(values)

        return result

    # 7. Action methods

    # 8. Business methods