odoo.define('barbershop.sign_in', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.sign_in = publicWidget.Widget.extend({
        selector: '.sign-in-barbershop',
        xmlDepControllerendencies: ['/barbershop/views/sign_up.xml'],
        events: {
            'input input[id=name]': '_validateAlphabetic',
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            console.log("init")
        },

        _validateAlphabetic: function (ev) {
            console.log('ev', ev)
            let currentTarget = $(ev.currentTarget)[0];
            let newValue = currentTarget.value.replace(/[0-9_.,&%$#@!^*()+=;:"<>?/\\|]/g, '');
            currentTarget.value = newValue;
        },

        _/* send: function () {

            this._rpc({
                route: '/make_appoiment/sent',
                params: {},
            }).then(function (actionData) {
                //return self.do_action(actionData);
            });
        } */
    });

});
