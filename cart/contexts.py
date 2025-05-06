from django.shortcuts import get_object_or_404
from courses.models import Course


def cart_contents(request):
    """ Makes the cart data available across all templates """

    cart_items = []
    # changed total to grand_total to match base.html
    grand_total = 0
    course_count = 0
    # get the cart from current section or an empty one
    cart = request.session.get('cart', {})

    for item_id in cart:
        # Gets the actual course object
        course = get_object_or_404(Course, pk=item_id)
        grand_total += course.price
        course_count += 1

        cart_items.append({
            'item_id': item_id,
            'course': course,
            'price': course.price,
        })

    context = {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'course_count': course_count,
    }

    return context
