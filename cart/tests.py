from django.test import TestCase, RequestFactory
from decimal import Decimal
from django.contrib.sessions.middleware import SessionMiddleware

from courses.models import Course
from bundles.models import Bundle
from cart.contexts import cart_contents

# Create your tests here.


class CartContextTests(TestCase):
    """
    Test that the cart processor:
    - retrieves cart items from session
    - fetches thec ourses and bundles
    - calculates the totals and product count
    """

    def setUp(self):
        self.factory = RequestFactory()

        # test course
        self.course = Course.objects.create(
            title="Test Course",
            price=Decimal("39.99"),
            description="description",
            content="content"
        )

        # test bundle
        self.bundle = Bundle.objects.create(
            title="Test Bundle",
            description="description",
            price=Decimal("19.00")
        )
        # add the course to the bundle
        self.bundle.courses.set([self.course])

        self.request = self.factory.get("/")
        middleware = SessionMiddleware(self.request)
        middleware.process_request(self.request)
        self.request.session.save()

        # add cart items to the session
        self.request.session['cart'] = {
                f'course_{self.course.id}': 1,
                f'bundle_{self.bundle.id}': 1,
            }
        self.request.session.save()

    def test_cart_with_course_and_bundle(self):
        # call the context processor function w the mock request
        context = cart_contents(self.request)

        # check that there's 2 items in the cart
        self.assertEqual(len(context['cart_items']), 2)

        # check that the total price is correcct
        self.assertEqual(
            context['grand_total'],
            self.course.price + self.bundle.price
        )

        # confirm that the item count is corrrect
        self.assertEqual(context['product_count'], 2)

        # check that the court title appears in the cart data
        self.assertEqual(
            context['cart_items'][0]['course'].title, "Test Course"
            )

        # check that the bundle title appears in the cart data
        self.assertEqual(
            context['cart_items'][1]['bundle'].title, "Test Bundle"
            )
