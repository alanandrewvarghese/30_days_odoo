from odoo import api, fields, models, _


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Books"
    
    name = fields.Char(string="Book Title", required=True)
    description = fields.Text(string="Description")
    isbn = fields.Char(string="ISBN")
    pages = fields.Integer(string="No. of Pages")
    is_published = fields.Boolean(string="Published", default=True)
    date_published = fields.Date(string="Published On")
    cover_price = fields.Float(string="Cover Price")
    category = fields.Selection(string="Category", selection=[
        ("fiction","Fiction"),
        ("non_fiction","Non Fiction")
    ])
    weight = fields.Float(string="Book Weight")
    author_id = fields.Many2one("res.partner", string="Author", required=True)
    tag_ids = fields.Many2many("library.book.tag", string="Tags")
    
    
class LibraryBookTag(models.Model):
    _name = "library.book.tag"
    _description = "Book Tags"
    
    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")