// Wait until DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Safely get Stripe keys
    var stripePublicKeyElement = document.getElementById('id_stripe_public_key');
    var clientSecretElement = document.getElementById('id_client_secret');
    
    if (!stripePublicKeyElement || !clientSecretElement) {
        console.error('Stripe keys not found in DOM');
        return;
    }

    var stripePublicKey = JSON.parse(stripePublicKeyElement.textContent);
    var clientSecret = JSON.parse(clientSecretElement.textContent);

    // Verify Stripe is loaded
    if (typeof Stripe === 'undefined') {
        console.error('Stripe.js not loaded!');
        return;
    }

    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();
    
    // Rest of your existing Stripe code...
    var style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };

    var card = elements.create('card', {style: style});
    card.mount('#card-element');

    // Handle realtime validation errors
    card.addEventListener('change', function (event) {
        var errorDiv = document.getElementById('card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });

    // Handle form submit
    var form = document.getElementById('payment-form');
    if (form) {
        form.addEventListener('submit', function(ev) {
            ev.preventDefault();
            card.update({ 'disabled': true});
            $('#submit-button').attr('disabled', true);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);

            var saveInfo = Boolean($('#id-save-info').attr('checked'));
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            var postData = {
                'csrfmiddlewaretoken': csrfToken,
                'client_secret': clientSecret,
                'save_info': saveInfo,
            };
            var url = '/checkout/cache_checkout_data/';

            $.post(url, postData).done(function () {
                stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: card,
                        billing_details: {
                            name: $.trim(form.full_name.value),
                            phone: $.trim(form.phone_number.value),
                            email: $.trim(form.email.value),
                            address:{
                                line1: $.trim(form.street_address1.value),
                                line2: $.trim(form.street_address2.value),
                                city: $.trim(form.town_or_city.value),
                                country: $.trim(form.country.value),
                                state: $.trim(form.county.value),
                            }
                        }
                    },
                    shipping: {
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        address: {
                            line1: $.trim(form.street_address1.value),
                            line2: $.trim(form.street_address2.value),
                            city: $.trim(form.town_or_city.value),
                            country: $.trim(form.country.value),
                            postal_code: $.trim(form.postcode.value),
                            state: $.trim(form.county.value),
                        }
                    },
                }).then(function(result) {
                    if (result.error) {
                        var errorDiv = document.getElementById('card-errors');
                        var html = `
                            <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                            </span>
                            <span>${result.error.message}</span>`;
                        $(errorDiv).html(html);
                        $('#payment-form').fadeToggle(100);
                        $('#loading-overlay').fadeToggle(100);
                        card.update({ 'disabled': false});
                        $('#submit-button').attr('disabled', false);
                    } else {
                        if (result.paymentIntent.status === 'succeeded') {
                            form.submit();
                        }
                    }
                });
            }).fail(function () {
                location.reload();
            });
        });
    }
});