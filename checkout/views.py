from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import PurchaseForm

# Create your views here.


def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect(reverse('courses'))

    form = PurchaseForm()
    context = {
        'form': form,
        'stripe_public_key': (
            'pk_test_51R9ARdRtqcHopRdxZBex957I6yZem6bq91iGObml'
            'JOBuSdHaGrYFpaISufuVnpzSMpvp3rjoVNHxtylAfRM5wYmY00BvLe0wR0'
            ),
        'client_secret': 'test client secret',
    }

    return render(request, 'checkout/checkout.html', context)
