from django.test import TestCase
from decimal import Decimal
from django.contrib.auth.models import User
from django.shortcuts import reverse
from unittest.mock import patch, MagicMock
from django.http import HttpResponse

from courses.models import Course
from bundles.models import Bundle
from checkout.models import Purchase, PurchaseItem
from checkout.forms import PurchaseForm
# Create your tests here.


# ------- Models
class PurchaseModelTests(TestCase):
    """
    Test that the Purchase and PurchaseItem models:
    - return the correct strings
    - geberate purchase nubers correctly
    - correctly calculate the grand totals
    """

    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(
            username='testEszter',
            password='testpassword'
            )

        # create a test course & bundle
        self.course = Course.objects.create(
            title="Test Course",
            price=Decimal("29.99"),
            description="description",
            content="content"
        )
        self.bundle = Bundle.objects.create(
            title="Test Bundle",
            price=Decimal("39.00"),
            description="description"
        )

        # create a purchase
        self.purchase = Purchase.objects.create(
            user=self.user,
            email="test@test.com",
            full_name="Test Eszter",
            street_address1="Test Street",
            city="Test City",
            postcode="424242",
            country="IE"
        )

    def test_purchase_str_returns_number(self):
        self.assertEqual(
            str(self.purchase), f'Purchase {self.purchase.purchase_number}'
            )

    def test_purchase_number_generated(self):
        self.assertIsNotNone(self.purchase.purchase_number)
        self.assertTrue(len(self.purchase.purchase_number) > 0)

    def test_update_total(self):
        # add a course item
        PurchaseItem.objects.create(
            purchase=self.purchase,
            course=self.course,
            quantity=1
            )
        # add a bundle item
        PurchaseItem.objects.create(
            purchase=self.purchase,
            bundle=self.bundle,
            quantity=1
            )
        # Update and check the purchase total
        self.purchase.update_total()
        expected_total = self.course.price + self.bundle.price
        self.assertEqual(self.purchase.grand_total, expected_total)

    def test_purchase_item_total_course(self):
        # Test item total calculation for a course
        item = PurchaseItem.objects.create(
            purchase=self.purchase,
            course=self.course,
            quantity=2
        )
        self.assertEqual(item.item_total, self.course.price * 2)

    def test_purchase_item_total_bundle(self):
        # Test item total calculation for a bundle
        item = PurchaseItem.objects.create(
            purchase=self.purchase,
            bundle=self.bundle,
            quantity=3
        )
        self.assertEqual(item.item_total, self.bundle.price * 3)

    def test_purchase_item_str_course(self):
        # test the __str__method for a course item
        item = PurchaseItem.objects.create(
            purchase=self.purchase,
            course=self.course,
            quantity=1
        )
        self.assertEqual(str(item), f'{self.course.title} (x1)')

    def test_purchase_item_str_bundle(self):
        # test the __str__method for a bundle item
        item = PurchaseItem.objects.create(
            purchase=self.purchase,
            bundle=self.bundle,
            quantity=2
        )
        self.assertEqual(str(item), f'{self.bundle.title} (x2)')

    # ------- Views
    """
    Test if:
    - Checkout view renders with valid cart
    - Checkout view handles empty cart
    - checkout_success marks purchase as paid and grants access
    """
    def test_checkout_view_with_empty_cart(self):
        """
        Test redirect if the cart is empty
        """
        self.client.login(
            username='testEszter',
            password='testpassword'
            )
        session = self.client.session
        session['cart'] = {}
        session.save()

        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/courses/')

    def test_checkout_success_view_is_paid(self):
        """
        Test if the checkout_success view updtaes payment status
        """
        # ensure that the purchase is unpaid first
        self.purchase.is_paid = False
        self.purchase.access_granted = False
        self.purchase.save()

        # log in user
        self.client.login(
            username='testEszter',
            password='testpassword'
            )

        response = self.client.get(
            reverse(
                'checkout_success',
                args=[self.purchase.purchase_number]
                )
        )
        self.assertEqual(response.status_code, 200)

        # refresh and check flags
        self.purchase.refresh_from_db()
        self.assertTrue(self.purchase.is_paid)
        self.assertTrue(self.purchase.access_granted)


# ------- Webhooks
class WebhookTests(TestCase):
    """
    Test that the webhook view:
    - correctly handles valid Stripe events
    - rejects invalid signatures
    """

    @patch('checkout.webhooks.StripeWH_Handler')
    @patch('checkout.views.stripe.Webhook.construct_event')
    def test_webhook_success_event(
        self,
        mock_construct_event,
        mock_handler_cls
    ):
        """
        Test that a successful payment_intent event returns http 200
        """
        # mock the event returned by stripe
        mock_event = {
            'type': 'payment_intent.succeeded',
            'data': {
                'object': {
                    'id': 'pi_test123',
                }
            }
        }

        # makes stripe construct_event return the mock_vent
        mock_construct_event.return_value = mock_event

        # mock the handler method that should be called
        mock_handler = MagicMock()
        mock_handler.handle_payment_intent_succeeded.return_value = (
            HttpResponse(status=200)
            )
        mock_handler_cls.return_value = mock_handler

        # send the request
        response = self.client.post(
            reverse('webhook'),
            data=b'{}',
            content_type='application/json',
            **{'HTTP_STRIPE_SIGNATURE': 'test_signature'}
        )

        # check that the correct handler methos was called
        mock_handler.handle_payment_intent_succeeded.assert_called_once_with(
            mock_event
            )
        self.assertEqual(response.status_code, 200)


# ------- Form
class PurchaseFormTest(TestCase):
    """
    Test that the PurchaseForm:
    - accepts valid input
    - rejects missing or invalid input
    """
    def setUp(self):
        # set up a valid data dictionery
        self.valid_data = {
            'email': 'test@test.com',
            'full_name': 'Test Name',
            'company_name': 'Test Co',
            'street_address1': '19 Test Street',
            'street_address2': 'Block 7',
            'city': 'Test City',
            'postcode': '424242',
            'country': 'IE'
        }

    def test_form_valid_data(self):
        """
        Form is valid with all required fields
        """
        form = PurchaseForm(data=self.valid_data)
        # should pass validation
        self.assertTrue(form.is_valid())

    def test_form_missing_required_field(self):
        """
        Form is invalid if required field is missing
        """
        invalid_data = self.valid_data.copy()
        # remove email
        invalid_data.pop('email')
        form = PurchaseForm(data=invalid_data)
        # should not pass
        self.assertFalse(form.is_valid())
        # email field should trigger error
        self.assertIn('email', form.errors)

    def test_form_invalid_country(self):
        """
        Form is invalid with missing country
        """
        invladi_data = self.valid_data.copy()
        # set country to blank
        invladi_data['country'] = ''
        form = PurchaseForm(data=invladi_data)
        # should not pass
        self.assertFalse(form.is_valid())
        # country field should raise an error
        self.assertIn('country', form.errors)
