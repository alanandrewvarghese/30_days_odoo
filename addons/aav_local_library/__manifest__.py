{
    "name": "Local Library Management",
    "version": "18.0.1.0.4",
    "summary": "Manage your library effortlessly.",
    "description": """
        This module helps librarians manage the book collection.
        Features:
        - Book list
        - Author management
    """,
    "author": "Alan Andrew Varghese",
    "website": "www.alanandrewvarghese.tech",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/library_book_views.xml",
        "views/res_partner_views.xml",
        "views/library_book_menus.xml",
    ],
    "demo": [
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}