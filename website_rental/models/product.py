# © 2022 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from datetime import date, datetime, timedelta
from dateutil import relativedelta

from odoo import _, fields, models, api

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_additionnal_combination_info(self, product_or_template, quantity, date, website):
        res = super()._get_additionnal_combination_info(product_or_template, quantity, date, website)

        product_or_template = product_or_template.sudo()
        res.update({
            'rental': product_or_template.rental,
        })
        return res


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _filter_by_availability(self, start_date, end_date):
        products = self
        for product in self:
            if product._get_availability_in_dates(start_date, end_date):
                continue
            else:
                products = products - product
        return products

    def _get_availability_in_dates(self, start_date, end_date=False, pricelist=False):
        rented_products = self.env['product.product'].search([
            ('rented_product_id', '=', self.id),
        ])
        if pricelist:
            self = self.with_context(pricelist=pricelist)
        delta = relativedelta.relativedelta(start_date, datetime.today())
        if delta.months >= 6:
            return False
        dates = [start_date]
        if end_date:
            end = end_date + timedelta(days=1)
            dates = [start_date + timedelta(days=x) for x in range(0, (end - start_date).days)]
        for cur_date in dates:
            is_available = True
            domain = [
                ("rental_product_id", "=", self.id),
                ("start_date", "<=", cur_date),
                ("end_date", ">=", cur_date - timedelta(days=1)),
                ("state", "in", ["ordered", "out", "sell_progress", "sold"]),
            ]
            rental = self.env["sale.rental"].sudo().search(domain)
            if rental:
                is_available = False
                return is_available

            lines_domain = [
                ("product_id", "in", rented_products.ids),
                ("start_date", "<=", cur_date),
                ("end_date", ">=", cur_date - timedelta(days=1)),
                ("validity_date", ">=", date.today()),
                ("state", "in", ["sent", "draft"]),
            ]
            order_lines = self.env["sale.order.line"].sudo().search(lines_domain)
            if order_lines:
                is_available = False
                return is_available

        return True
