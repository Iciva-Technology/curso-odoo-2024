odoo.define('barbershop.make_appointment', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.make_appointment = publicWidget.Widget.extend({
        selector: '.make-appointment-barbershop',
        events: {
            'submit #make_appointment_form': '_onFormSubmit',
            'change #barber_id': '_onBarberChange',
            'change #service_ids': '_onServicesChange',
            'change #start_at': '_validateDateTime'
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            console.log("Appointment form initialized");
        },

        start: function () {
            this._super.apply(this, arguments);
            this.$form = this.$('#make_appointment_form');
            this.$submitButton = this.$('#appoiment_send_button');
            this.$resultSpan = this.$('#s_website_form_result');
            return this._super();
        },

        _onFormSubmit: function (ev) {
            ev.preventDefault();

            if (!this._validateForm()) {
                return false;
            }

            this._disableSubmitButton();
            this._sendAppointment();
        },

        _validateForm: function () {
            const partnerId = this.$('#partner_id').val();
            const barberId = this.$('#barber_id').val();
            const startAt = this.$('#start_at').val();
            const serviceIds = this.$('#service_ids').val();

            if (!partnerId || !barberId || !startAt || !serviceIds || serviceIds.length === 0) {
                this._showError('Por favor complete todos los campos requeridos');
                return false;
            }

            return true;
        },

        _validateDateTime: function (ev) {
            const selectedDate = new Date($(ev.currentTarget).val());
            const now = new Date();

            if (selectedDate < now) {
                this._showError('La fecha y hora seleccionada debe ser posterior a la actual');
                $(ev.currentTarget).val('');
                return false;
            }

            // Clear any previous error messages
            this._clearError();
            return true;
        },

        _onBarberChange: function (ev) {
            // Here you could add logic to check barber availability
            // and update available time slots
            this._clearError();
        },

        _onServicesChange: function (ev) {
            // Here you could add logic to calculate total duration
            // and update available time slots based on selected services
            this._clearError();
        },

        _sendAppointment: function () {
            const self = this;
            const formData = new FormData(this.$form[0]);
            console.log(formData.get('start_at'));

            this._rpc({
                route: '/make_appointment/sent',
                params: {
                    data: {
                        partner_id: formData.get('partner_id'),
                        barber_id: formData.get('barber_id'),
                        start_at: formData.get('start_at'),
                        service_ids: formData.getAll('service_ids')
                    }
                },
            }).then(function (result) {
                if (result.success) {
                    self._showSuccess('Cita reservada exitosamente');
                    setTimeout(function () {
                        window.location.href = '/';
                    }, 2000);
                } else {
                    self._showError(result.error || 'Error al reservar la cita');
                    self._enableSubmitButton();
                }
            }).catch(function (error) {
                self._showError('Error de conexión. Por favor intente nuevamente');
                self._enableSubmitButton();
            });
        },

        _showError: function (message) {
            this.$resultSpan.removeClass('text-success').addClass('text-danger').text(message);
        },

        _showSuccess: function (message) {
            this.$resultSpan.removeClass('text-danger').addClass('text-success').text(message);
        },

        _clearError: function () {
            this.$resultSpan.removeClass('text-danger text-success').text('');
        },

        _disableSubmitButton: function () {
            this.$submitButton.prop('disabled', true).text('Procesando...');
        },

        _enableSubmitButton: function () {
            this.$submitButton.prop('disabled', false).text('Reservar');
        }
    });
});