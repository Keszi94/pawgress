from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST

from courses.models import Course

# Create your views here.


def view_cart(request):
    """ A viw that renders the cart contents page """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """
    Adds a course to the cart
    Only one of each course can be added
    """
    course = Course.objects.get(pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    # convert item_id to a string
    item_id = str(item_id)

    # Only add a course if it's not in the cart already
    if item_id not in cart:
        cart[item_id] = 1
        messages.success(request, f'{course.title} has been added to your bag!')

    request.session['cart'] = cart

    return redirect(redirect_url)


# this view handles only POST requests
@require_POST
def remove_from_cart(request, item_id):
    """ Removes a course from the shopping cart """

    try:
        cart = request.session.get('cart', {})

        # removes the item if it IS in the cart
        if item_id in cart:
            cart.pop(item_id)

        # Saves the updated cart
        request.session['cart'] = cart

        # Returns success response
        return HttpResponse(status=200)

    # 'e' for error message display
    except Exception as e:
        return HttpResponse(status=500)
