##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2025 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Website rental",
    "version": "18.0.0.0.1",
    "summary": "Website rental",
    "category": "Ecommerce",
    "author": "Comunitea",
    "website": "https://www.comunitea.com",
    "license": "AGPL-3",
    "depends": [
        "sale_rental",
        "website_sale",
    ],
    "data": [
        "templates/rental_list.xml",
        "templates/product.xml",
        "templates/cart_lines.xml",
        "templates/product_list.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            "/website_rental/static/src/js/rental_date.js",
            "/website_rental/static/src/js/variant_mixin.js",
            "/website_rental/static/src/js/product_detail.js",
        ],
    },
    "images": [],
    "installable": True,
    "application": True,
}
