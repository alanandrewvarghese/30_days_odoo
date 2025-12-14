from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit="res.partner"
    
    authored_book_ids = fields.One2many("library.book", "author_id", string="Authored Books")
    is_author = fields.Boolean(string="Is Author", compute="_compute_is_author", store=True, readonly=True)
    total_pages = fields.Integer(string="Total Pages", compute="_compute_total_pages", store=True, readonly=True)
    
    @api.depends("authored_book_ids")
    def _compute_is_author(self):
        for partner in self:
            if partner.authored_book_ids:
                partner.is_author = True
            else:
                partner.is_author = False
                
    @api.depends("authored_book_ids", "authored_book_ids.pages")
    def _compute_total_pages(self):
        for partner in self:
            if partner.authored_book_ids:
                partner.total_pages = sum(partner.authored_book_ids.mapped('pages'))
            else:
                partner.total_pages = 0
                