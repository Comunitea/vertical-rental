/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteRentalPage = publicWidget.Widget.extend({
    selector: "form.rental_form",
    events: {
        "click button.reset_dates": "_onClickResetDates",
    },

    init: function (parent, editableMode) {
        this._super.apply(this, arguments);
    },
    start: function () {
        var _this = this;
        this._super.apply(this, arguments);
    },
    _onClickResetDates: function (event) {
        var self = this;
        event.preventDefault();
        event.stopPropagation();
        var form = $(event.currentTarget).closest('form');
        var inputs = form.find('input[type="date"]');
        inputs.each(function () {
            $(this).val($(this).attr("min"));
        });
        form.submit();
    },
});
