from django.test import TestCase
from decimal import Decimal
from django.contrib.auth.models import User

from courses.models import Course
from bundles.models import Bundle
from checkout.models import Purchase, PurchaseItem
# Create your tests here.


# ------- Model
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
            username='tester', password='testpassword'
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
