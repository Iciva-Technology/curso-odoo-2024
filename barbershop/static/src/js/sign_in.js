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

    });

});

odoo.define('barbershop.reservation', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.reservation = publicWidget.Widget.extend({
        selector: '.reservation-barbershop',
        events: {
            'click button.submit-form': '_submitForm',
        },

        _submitForm: function (ev) {
            ev.preventDefault();

            const partnerId = $('#partner_id').val();
            const serviceId = $('#service_id').val();
            const barberId = $('#employee_id').val();
            const startAt = $('#start_at').val();

            // Validación básica en el cliente
            if (!partnerId || !serviceId || !startAt) {
                alert("Todos los campos son obligatorios.");
                return;
            }

            this._rpc({
                route: '/create_appointment',
                params: {data: {
                    partner_id: partnerId,
                    service_id: serviceId,
                    employee_id: barberId,
                    start_at: startAt,
                }
                },
            }).then(function (response) {
                if (response.error) {
                    alert(response.error);
                } else {
                    alert(response.success);
                    window.location.href = '/reservation';
                }
            }).catch(function (err) {
                alert('Error al procesar la solicitud.');
                console.error(err);
            });
        },
    });

    return publicWidget.registry.reservation;
});