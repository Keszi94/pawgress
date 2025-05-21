from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from decimal import Decimal
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User

from courses.models import Course, Category
from bundles.models import Bundle
from cart.contexts import cart_contents
from checkout.models import Purchase, PurchaseItem

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


class CartViewTests(TestCase):
    """
    Test if the cart view:
    - renders correctly
    - Cours and bundles can be added
    - Course/Bundle can be removes
    """
    def setUp(self):
        self.client = Client()

        # test user and login
        self.user = User.objects.create_user(
            username='tester',
            password='testpassword'
            )
        self.client.login(
            username='tester', password='testpassword'
            )

        self.category = Category.objects.create(name="Training")
        # test course
        self.course = Course.objects.create(
            title="Test Course",
            price=Decimal("39.99"),
            description="description",
            content="content",
            category=self.category
        )
        # test bundle
        self.bundle = Bundle.objects.create(
            title="Test Bundle",
            description="description",
            price=Decimal("19.00")
        )
        # add the course to the bundle
        self.bundle.courses.set([self.course])

    def test_view_cart_template(self):
        """
        View cart returns http 200 and it uses the correct template
        """
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')

    def test_add_course_to_cart(self):
        """
        Add a course to the cart
        """
        self.client.post(
            reverse(
                'add_to_cart',
                args=[self.course.id]), {
                    'item_type': 'course',
                    'redirect_url': reverse('courses')
                })
        session = self.client.session
        self.assertIn(f'course_{self.course.id}', session['cart'])

    def test_remove_course_from_cart(self):
        """
        Remove a course from the cart
        """
        session = self.client.session
        session['cart'] = {f'course_{self.course.id}': 1}
        session.save()

        response = self.client.post(
            reverse('remove_from_cart', args=[f'course_{self.course.id}'])
            )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            f'course_{self.course.id}', self.client.session.get('cart', {})
            )

    def test_prevent_adding_already_owned_course(self):
        """
        Already purchased courses should not be added to the cart again
        """
        # simulate a purchase
        purchase = Purchase.objects.create(
            user=self.user,
            access_granted=True
            )
        PurchaseItem.objects.create(purchase=purchase, course=self.course)

        response = self.client.post(
            reverse('add_to_cart', args=[self.course.id]), {
                'item_type': 'course',
                'redirect_url': reverse('courses')
            })

        session = self.client.session
        self.assertNotIn(f'course_{self.course.id}', session.get('cart', {}))

        messages = list(response.wsgi_request._messages)
        self.assertTrue(
            any("already own the course" in str(m) for m in messages)
            )
