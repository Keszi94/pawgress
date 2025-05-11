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
    }

    return render(request, 'checkout/checkout.html', context)
