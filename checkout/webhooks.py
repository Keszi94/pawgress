# Code based on Boutique Ado wt project
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .webhook_handler import StripeWH_Handler


@require_POST
@csrf_exempt
def webhook(request):
    """
    Handle Stripe webhooks (payment success/fail)
    """

    # Set up Stripe API key and wh secrett
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the payload and signature header from Stripe
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    # Try event from Stripe
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:  # noqa: F841
        # Payload invalid
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:  # noqa: F841
        # signature doesnt match
        return HttpResponse(status=400)
    except Exception as e:
        # all unexpected errors
        return HttpResponse(content=e, status=400)

    # Stripe webhook handler instance
    handler = StripeWH_Handler(request)

    # Map spec Stripe event types to handler methods
    event_map = {
        'payment_intent.succeeded':
            handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed':
            handler.handle_payment_intent_failed,
    }

    # Get the event type from payload
    event_type = event['type']

    # Use the matching handler, if not available use generic
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the handler function and return response
    response = event_handler(event)
    return response
