from django.shortcuts import render, redirect

# Create your views here.


def view_cart(request):
    """ A viw that renders the cart contents page """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """
    Adds a course to the cart
    Only one of each course can be added
    """
    redirect_url = request.POST.get('redirect_url')

    cart = request.session.get('cart', {})
    # convert item_id to a string
    item_id = str(item_id)

    # Only add a course if it's not in the cart already
    if item_id not in cart:
        cart[item_id] = 1

    request.session['cart'] = cart
    print(request.session['cart'])

    return redirect(redirect_url)
