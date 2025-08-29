/** @odoo-module **/
import {_t} from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteRentalProduct = publicWidget.Widget.extend({
    selector: "#product_detail",
    events: {
        "click button.reset_dates": "_onClickResetDates",
        "change form input[name='start'], form input[name='end']": "_onChangeDate",
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
    },
    _onChangeDate(event) {
        var inputs = $(
            '#product_detail form input[name="start"], #product_detail form input[name="end"]'
        );
        var error_div = $(event.currentTarget).closest('form').find('.rental_error');
        var submit_button = $(event.currentTarget).closest('form').find('.book_button');
        error_div.empty();

        if (inputs[0].value && inputs[1].value) {
            if (inputs[0].value > inputs[1].value) {
                var error_message = _t("Start date must be before end date");
                if (error_div) {
                    error_div.prepend(
                        '<div class="alert alert-danger rental_error" role="alert">' +
                            error_message +
                        "</div>"
                    );
                }
                submit_button.prop("disabled", true);
                return;
            } else {
                error_div.empty();
                submit_button.prop("disabled", false);
            }
        }
    }
});
