# Code based on Boutique Ado wt project
import stripe
import json
import time

from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Purchase, PurchaseItem
from courses.models import Course
from bundles.models import Bundle


class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook
        """

        intent = event.data.object
        pid = intent.id
        cart = json.loads(intent.metadata.cart)
        save_info = intent.metadata.save_info
        username = intent.metadata.username

        user = None
        if username != 'AnonymousUser':
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

        # Get charge object from Stripe
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        billing_details = stripe_charge.billing_details
        grand_total = round(stripe_charge.amount / 100, 2)

        # Converts empty strings to None
        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None

        # Check if order already exists
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                purchase = Purchase.objects.get(
                    user=user,
                    email__iexact=billing_details.email,
                    full_name__iexact=billing_details.name,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2 or "",
                    city__iexact=billing_details.address.city,
                    postcode__iexact=billing_details.address.postal_code,
                    country__iexact=billing_details.address.country,
                    grand_total=grand_total,
                    original_cart=json.dumps(cart),
                    stripe_payment_intent=pid,
                )
                order_exists = True
                break
            except Purchase.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} |'
                f' SUCCESS: Order already in database',
                status=200
            )

        # Order not found
        try:
            purchase = Purchase.objects.create(
                email=billing_details.email,
                full_name=billing_details.name,
                street_address1=billing_details.address.line1,
                street_address2=billing_details.address.line2,
                city=billing_details.address.city,
                postcode=billing_details.address.postal_code,
                country=billing_details.address.country,
                grand_total=grand_total,
                original_cart=json.dumps(cart),
                stripe_payment_intent=pid,
            )

            for item_key, item_data in cart.items():
                if '_' not in item_key:
                    continue
                item_type, item_id = item_key.split('_', 1)

                if item_type == 'course':
                    course = Course.objects.get(pk=item_id)
                    PurchaseItem.objects.create(
                        purchase=purchase,
                        course=course,
                        quantity=1
                    )
                elif item_type == 'bundle':
                    bundle = Bundle.objects.get(pk=item_id)
                    PurchaseItem.objects.create(
                        purchase=purchase,
                        bundle=bundle,
                        quantity=1
                    )
            return HttpResponse(
                content=f'Webhook received: {event["type"]} |'
                f' SUCCESS: Created order in webhook ({pid})',
                status=200
            )
        except Exception as e:
            if 'purchase' in locals():
                purchase.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {str(e)}',
                status=500
            )

    def handle_payment_intent_failed(self, event):
        """
        Handle the payment_inent.payment_failed webhook
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
