// https://docs.stripe.com/payments/accept-a-payment
// https://github.com/Code-Institute-Solutions/boutique_ado_v1_sourcecode/tree/main/13-setting-up-payments/13-02-integrating-stripe-elements-for-cecure-card-input
 

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements()

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

// Handle real time validation errors on card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
        <span class="icon"  role="alert">
            <i class="fas fa-exclamation-circle"></i>
        </span>
        <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submission
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true });
    $('#submit-button').attr('disabled', true);

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var saveInfo = Boolean($('#id-save-info').prop('checked'));
    var url = '/checkout/cache_checkout_data/';
    var postData = {
        csrfmiddlewaretoken: csrfToken,
        client_secret: clientSecret,
        save_info: saveInfo,
    };

    $.post(url, postData)
        .done(function () {
        // confirm card payment
            stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    email: $.trim(form.email.value),
                    name: $.trim(form.full_name.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.city.value),
                        postal_code: $.trim(form.postcode.value),
                        country: $.trim(form.country.value),
                    }
                }
            }
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>
                `;
                $(errorDiv).html(html);
                card.update({ 'disabled': false });
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    })
    .fail(function () {
        // if failed, reload page to show error
        location.reload();
    });
});