from django.shortcuts import get_object_or_404
from courses.models import Course
from bundles.models import Bundle


def cart_contents(request):
    """
    Makes the cart data, both courses and bundles
    available across all templates
    """

    cart_items = []
    # changed total to grand_total to match base.html
    grand_total = 0
    product_count = 0
    # get the cart from current section or an empty one
    cart = request.session.get('cart', {})

    for item_key, quantity in cart.items():
        if '_' not in item_key:
            continue
        item_type, item_id = item_key.split('_', 1)

        if item_type == 'course':
            # Gets the actual course object
            course = get_object_or_404(Course, pk=item_id)
            grand_total += course.price
            product_count += 1
            cart_items.append({
                'item_key': item_key,
                'course': course,
                'price': course.price,
            })

        elif item_type == 'bundle':
            bundle = get_object_or_404(Bundle, pk=item_id)
            grand_total += bundle.price
            cart_items.append({
                'item_key': item_key,
                'bundle': bundle,
                'price': bundle.price,
            })

    context = {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'product_count': product_count,
    }

    return context
