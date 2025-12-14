from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit="res.partner"
    
    authored_book_ids = fields.One2many("library.book", "author_id", string="Authored Books")