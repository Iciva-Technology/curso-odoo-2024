odoo.define('barbershop.appointment_consultation', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.appointment_consultation = publicWidget.Widget.extend({
        selector: '.appointment-consultation-barbershop',
        xmlDepControllerendencies: ['/barbershop/views/appointment_consultation.xml'],
        events: {
            'click button[id=search-appointment]': '_onSearchAppointment',
        },


        init: function (parent, options) {
            this._super.apply(this, arguments);
            console.log('HOLAA SOY EL INIT ')

        },
        _onSearchAppointment: function () {
            var appointmentNumber = this.$('#appointment-number').val();
            console.log('HOLA')
            if (!appointmentNumber) {
                alert('Por favor, ingrese el número de la cita.');
                return;
            }
            var self = this;
            ajax.jsonRpc('/get_appointment_details', 'call', {
                appointment_number: appointmentNumber,
            }).then(function (data) {
                if (data.success) {
                    self._showAppointmentDetails(data.details);
                } else {
                    alert('Cita no encontrada.');
                }
            });
        },

        _showAppointmentDetails: function (details) {
            this.$('#appointment-client').text(details.client);
            this.$('#appointment-date').text(details.date);
            this.$('#appointment-service').text(details.service);
            this.$('#appointment-details').show();
        },


    });

});
