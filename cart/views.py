from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from courses.models import Course
from bundles.models import Bundle

# Create your views here.


def view_cart(request):
    """ A viw that renders the cart contents page """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """
    Adds a course or a bundle to the cart
    Only one of each course can be added
    Can't add a course it it's already in a bundle in the cart
    Can't add a bundle it it has a course already in the cart
    """

    item_type = request.POST.get('item_type', 'course')
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    # convert item_id to a string
    item_key = f"{item_type}_{item_id}"

    # check if a course is already in a bundle that's in the cart
    if item_type == 'course':
        course = get_object_or_404(Course, pk=item_id)
        for key in cart:
            # only check bundles
            if key.startswith('bundle_'):
                bundle_id = key.split('_')[1]
                bundle = get_object_or_404(Bundle, pk=bundle_id)
                # if the course is in a bundle in the cart, block from adding
                if course in bundle.courses.all():
                    messages.info(
                        request,
                        f'"{course.title}" is already included in the bundle '
                        f'"{bundle.title}" in your cart.'
                    )
                    return redirect(redirect_url)

    # check if a bundle has a course that is already added in the cart
    if item_type == 'bundle':
        bundle = get_object_or_404(Bundle, pk=item_id)
        for course in bundle.courses.all():
            course_key = f"course_{course.id}"
            if course_key in cart:
                messages.info(
                    request,
                    f'Bundle "{bundle.title}" already includes the course '
                    f'"{course.title}", which is in your cart.'
                )
                return redirect(redirect_url)

    # Only add an item if it's not in the cart already
    if item_key not in cart:
        cart[item_key] = 1

        if item_type == 'course':
            course = get_object_or_404(Course, pk=item_id)
            messages.success(
                request,
                f'{course.title} has been added to your cart!'
                )
        elif item_type == 'bundle':
            bundle = get_object_or_404(Bundle, pk=item_id)
            messages.success(
                request,
                f'Bundle "{bundle.title}" has been added to your cart!'
                )
    else:
        if item_type == 'course':
            course = get_object_or_404(Course, pk=item_id)
            messages.info(request, f'{course.title} is already in your cart!')
        elif item_type == 'bundle':
            bundle = get_object_or_404(Bundle, pk=item_id)
            messages.info(
                request,
                f'Bundle "{bundle.title}" is already in your cart!')

    request.session['cart'] = cart
    return redirect(redirect_url)


# this view handles only POST requests
@require_POST
def remove_from_cart(request, item_key):
    """ Removes a course or bundle from the shopping cart """

    try:
        cart = request.session.get('cart', {})

        # removes the item if it IS in the cart
        if item_key in cart:
            item_type, item_id = item_key.split('_')

            if item_type == 'course':
                course = get_object_or_404(Course, pk=item_id)
                messages.success(
                    request,
                    f'{course.title} has been successfully removed '
                    f'from your cart!'
                    )
            elif item_type == 'bundle':
                bundle = get_object_or_404(Bundle, pk=item_id)
                messages.success(
                    request,
                    f'Bundle "{bundle.title}" has been successfully removed '
                    f'from your cart!'
                    )

            cart.pop(item_key)
            # Saves the updated cart
            request.session['cart'] = cart

        # Returns success response
        return HttpResponse(status=200)

    # 'e' for error message display
    except Exception as e:
        messages.error(
            request,
            f"Something went wrong while removing "
            f"{course.title} from your cart: {e}"
            )
        return HttpResponse(status=500)
    # remove {e} later before deployment
