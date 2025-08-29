import json
import base64
from datetime import date, datetime, timedelta
import locale
from io import BufferedReader

from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import Website
from odoo.addons.http_routing.models.ir_http import slug

class Website(Website):
    def get_rental_domain(self):
        domain = [
            ("website_published", "=", True),
            ("rental", "=", True),
        ]
        return domain

    @http.route(['/rental', '/rental/page/<int:page>'], csrf=False, auth='public', website=True, type='http', methods=['GET', 'POST'])
    def get_rental_product_list(self, page=0, **post):
        values = {}
        domain = self.get_rental_domain()
        products = request.env["product.product"]
        products_count = products.search_count(domain)
        url = "/rental"
        start_date = datetime.now()
        min_date = start_date
        end_date = start_date + timedelta(1)
        min_end_date = end_date
        max_date = start_date + timedelta(200)
        pager = request.website.pager(
            url=url, total=products_count, page=page, step=15, scope=7, url_args=post
        )
        products = products.sudo().search(
            domain, limit=15, offset=pager["offset"]
        )

        if post.get("start"):
            start_date = datetime.strptime(post.get("start"), "%Y-%m-%d").date()
        if post.get("end"):
            end_date = datetime.strptime(post.get("end"), "%Y-%m-%d").date()

        if post.get("start") or post.get("end"):
            products = products._filter_by_availability(start_date, end_date)

        values['start_date'] = start_date.strftime('%Y-%m-%d')
        values['end_date'] = end_date.strftime('%Y-%m-%d')
        values['min_date'] = min_date.strftime('%Y-%m-%d')
        values['min_end_date'] = min_end_date.strftime('%Y-%m-%d')
        values['max_date'] = max_date.strftime('%Y-%m-%d')
        values['text_start_date'] = start_date.strftime('%d %b')
        values['text_end_date'] = end_date.strftime('%d %b')
        values['object_list'] = products
        return request.render('website_rental.rental_list', values)


class WebsiteSaleRental(WebsiteSale):

    def product(self, product, category='', search='', **kwargs):
        res = super(WebsiteSaleRental, self).product(product, category, search, **kwargs)
        if product.rental:
            start_date = datetime.now().date()
            end_date = (datetime.now() + timedelta(1)).date()
            if kwargs.get("start"):
                start_date = datetime.strptime(kwargs.get("start"), "%Y-%m-%d").date()
            if kwargs.get("end"):
                end_date = datetime.strptime(kwargs.get("end"), "%Y-%m-%d").date()
            res.qcontext['rental'] = True
            res.qcontext['start_date'] = start_date
            res.qcontext['end_date'] = end_date
            res.qcontext['min_date'] = start_date
            res.qcontext['max_date'] = (start_date + timedelta(200))
            res.qcontext['available_on_dates'] = product.product_variant_id._get_availability_in_dates(start_date, end_date)
        print("res.qcontext: {}".format(res.qcontext))
        return res

    def cart_update(
        self, product_id, add_qty=1, set_qty=0,
        product_custom_attribute_values=None, no_variant_attribute_values=None,
        express=False, **kwargs
    ):
        product = request.env['product.product'].browse(int(product_id))
        if not product.rental:
            return super(WebsiteSaleRental, self).cart_update(
                product_id, add_qty=add_qty, set_qty=set_qty,
                product_custom_attribute_values=product_custom_attribute_values,
                no_variant_attribute_values=no_variant_attribute_values,
                express=express, **kwargs
            )
        start_date = kwargs.get("start")
        end_date = kwargs.get("end")

        if not start_date or not end_date:
            return request.redirect(product.product_tmpl_id.website_url)

        rental_service = product.rental_service_ids.filtered(
            lambda x: not x.website_id.id or x.website_id.id in [False, request.website.id] and x._get_availability_in_dates(
                datetime.strptime(start_date, "%Y-%m-%d").date(),
                datetime.strptime(end_date, "%Y-%m-%d").date()
            )
        )

        if rental_service:
            res = super(WebsiteSaleRental, self).cart_update(
                rental_service[0].id, add_qty=add_qty, set_qty=set_qty,
                product_custom_attribute_values=product_custom_attribute_values,
                no_variant_attribute_values=no_variant_attribute_values,
                express=express, **kwargs
            )
            sale_order = request.website.sale_get_order(force_create=True)
            sale_order.write({
                'type_id': request.env.ref('rental_base.rental_sale_type').id,
            })
            return res
        url = "{}?start={}&end={}".format(
            product.product_tmpl_id.website_url,
            start_date,
            end_date
        )
        return request.redirect(url)
