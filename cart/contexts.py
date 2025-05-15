from courses.models import Course
from bundles.models import Bundle


def cart_contents(request):
    """
    Makes the cart data, both courses and bundles
    available across all templates
    """

    cart_items = []
    grand_total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for item_key, quantity in cart.items():
        if '_' not in item_key:
            continue
        item_type, item_id = item_key.split('_', 1)

        if item_type == 'course':
            try:
                course = Course.objects.get(pk=item_id)
                grand_total += course.price
                product_count += 1
                cart_items.append({
                    'item_key': item_key,
                    'course': course,
                    'price': course.price,
                })
            except Course.DoesNotExist:
                continue  # Skip deleted course

        elif item_type == 'bundle':
            try:
                bundle = Bundle.objects.get(pk=item_id)
                grand_total += bundle.price
                product_count += 1
                cart_items.append({
                    'item_key': item_key,
                    'bundle': bundle,
                    'price': bundle.price,
                })
            except Bundle.DoesNotExist:
                continue  # Skip deleted bundle

    context = {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'product_count': product_count,
    }

    return context
