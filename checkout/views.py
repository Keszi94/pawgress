import json
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import PurchaseForm
from .models import PurchaseItem, Purchase
from cart.contexts import cart_contents
from courses.models import Course
from bundles.models import Bundle

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment can not be \
                       processed right now. Please try agen later.')
        return HttpResponse(content=e, status=400)


@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect(reverse('courses'))

    if request.method == 'POST':
        form_data = {
            'email': request.POST['email'],
            'full_name': request.POST['full_name'],
            'company_name': request.POST['company_name'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'city': request.POST['city'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }

        form = PurchaseForm(form_data)

        if form.is_valid():
            purchase = form.save(commit=False)

            # save logged-in user
            if request.user.is_authenticated:
                purchase.user = request.user

            purchase.stripe_payment_intent = (
                request.POST.get('client_secret').split('_secret')[0]
                )
            purchase.original_cart = json.dumps(cart)
            purchase.save()

            # create items
            for item_key, item_data in cart.items():
                if '_' not in item_key:
                    continue
                item_type, item_id = item_key.split('_', 1)

                if item_type == 'course':
                    course = get_object_or_404(Course, pk=item_id)
                    PurchaseItem.objects.create(
                        purchase=purchase,
                        course=course,
                        quantity=1
                    )
                elif item_type == 'bundle':
                    bundle = get_object_or_404(Bundle, pk=item_id)
                    PurchaseItem.objects.create(
                        purchase=purchase,
                        bundle=bundle,
                        quantity=1
                    )

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse(
                    'checkout_success', args=[purchase.purchase_number]
                    ))
        else:
            messages.error(
                request,
                'There was an error in your form.'
                'Please double check your information.'
                )
    else:
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


@login_required
def checkout_success(request, purchase_number):
    """
    Handles successful checkouts
    """

    purchase = get_object_or_404(Purchase, purchase_number=purchase_number)

    messages.success(
        request,
        f'Your order was processed successfully! Your order number is: '
        f' {purchase_number}. A confirmation email will be sent '
        f'to {purchase.email}.'
        )

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'purchase': purchase,
    }

    return render(request, template, context)
