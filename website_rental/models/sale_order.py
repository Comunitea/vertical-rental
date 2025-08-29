import logging

import dateutil.parser as dparser
from datetime import timedelta, datetime, date

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_order_line_values(
        self, product_id, quantity, linked_line_id=False,
        no_variant_attribute_values=None, product_custom_attribute_values=None,
        **kwargs
    ):
        res = super()._prepare_order_line_values(
            product_id, quantity, linked_line_id=linked_line_id,
            no_variant_attribute_values=no_variant_attribute_values,
            product_custom_attribute_values=product_custom_attribute_values,
            **kwargs
        )
        start_date = kwargs.get("start")
        end_date = kwargs.get("end")
        if not start_date or not end_date:
            return res
        product = self.env['product.product'].browse(product_id)
        days = (
            datetime.strptime(end_date, "%Y-%m-%d").date() - datetime.strptime(start_date, "%Y-%m-%d").date()
        )

        if product.rented_product_id:
            res.update({
                'start_date': dparser.parse(kwargs.get("start"), fuzzy=True),
                'end_date': dparser.parse(kwargs.get("end"), fuzzy=True),
                'product_uom_qty': days.days,
            })

        return res

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    validity_date = fields.Date(related="order_id.validity_date")
