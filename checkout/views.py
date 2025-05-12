import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import PurchaseForm
from cart.contexts import cart_contents

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect(reverse('courses'))

    form = PurchaseForm()

    # Get current cart totals
    cart_context = cart_contents(request)
    total = cart_context['grand_total']
    stripe_total = round(total * 100)

    # Create payment intent
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    client_secret = intent.client_secret

    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing. Did u forget to set it?'
        )

    template = 'checkout/checkout.html'
    context = {
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret
    }

    return render(request, template, context)
