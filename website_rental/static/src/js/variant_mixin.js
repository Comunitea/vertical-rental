/** @odoo-module **/

import VariantMixin from "@website_sale_stock/js/variant_mixin";
import "@website_sale/js/website_sale";

const oldChangeCombinationStock = VariantMixin._onChangeCombinationStock;
/**
 *
 * @override
 */
VariantMixin._onChangeCombinationStock = function (ev, $parent, combination) {
    oldChangeCombinationStock.apply(this, arguments);
    if (combination.rental) {
        let ctaWrapper = $parent[0].querySelector('#o_wsale_cta_wrapper');
        ctaWrapper.classList.add('d-none');
    }
};
