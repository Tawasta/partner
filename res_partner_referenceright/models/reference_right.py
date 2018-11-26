from odoo import api, models, fields
from odoo import SUPERUSER_ID
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class reference_right(models.Model):
    _name = "res.partner.reference_right"
    _order = "company_id, code"
    
    ''' When module is installed, fetch all companies and create reference rights '''
    @api.model
    def _init_reference_rights(self, context=None):
        ref_rights = {
            'reference_right_allowed': _('Allowed'),
            'reference_right_ask': _('Ask'),
            'reference_right_no': _('No Right'),
        }

        company_obj = self.env.get('res.company')
        refright_obj = self.env.get('res.partner.reference_right')
        
        company_ids = company_obj.sudo().search([], order='id')
        
        for company in company_obj.sudo().browse([], company_ids):
            for key, value in ref_rights.iteritems():
                vals = {'code': key, 'name': value, 'company_id': company.id}
                refright_obj.sudo().create(vals, context)
        
        return True
    @api.model
    def name_get(self, context=None):
        # Decide if there is more than one company
        company_obj = self.env.get('res.company')
        company_count = company_obj.sudo().search_count([])

        res = []
        for record in self.browse([context]):
            name = ''
            
            if record.company_id.name and company_count > 1:
                name += '%s - ' % (record.company_id.name)
            
            name += '%s' % (record.name)
            
            res.append((record.id, name))
        
        return res
    
    @api.model
    def name_search(self, args, name, operator='ilike', limit=20):
        if args:
            try:
                refright_ids = args[0][2]
                refrights = self.browse([refright_ids])
            
                company_ids = []
                for refright in refrights:
                    company_ids.append(refright.company_id.id)
                
                args = [('company_id', 'not in', company_ids)]
            except IndexError:
                # No refright ids
                pass
        
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            ids = self.search(['|', ('name', operator, name), ('company_id.name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search([] + args, limit=limit, context=context)
            
        return self.name_get(ids, context)
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, context=None, count=False):
        if args and 0 in args and 2 in args[0]:
            refright_ids = args[0][2]
            refrights = self.browse([refright_ids, context])
            
            company_ids = []
            for refright in refrights:
                company_ids.append(refright.company_id.id)
            
            args = [('company_id', 'not in', company_ids)]

        return super(reference_right, self).search([] + args, offset, limit, order, context=context, count=count)
    
        name = fields.Char(string='Reference right', size=128, translate=True),
        code = fields.Char(string='Code', size=128),          
        company_id = fields.Many2one('res.company', 'Company'),
        partner_ids = fields.Many2many('res.partner', id1='referenceright', id2='partner_id', string='Partners'),
    
    _sql_constraints = [
        ('company_code_unique', 'unique(company_id, code)', 'This company already has a reference right with this code.')
    ]
