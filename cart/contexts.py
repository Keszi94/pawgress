

def cart_contents(request):
    """ Makes the cart data available across all templates """

    cart_items = []
    total = 0
    course_count = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'course_count': course_count,
    }

    return context
