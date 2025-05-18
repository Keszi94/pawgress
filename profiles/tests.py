from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from django.urls import reverse

from courses.models import Course
from profiles.models import CourseCompletion
from checkout.models import Purchase, PurchaseItem

# Create your tests here.


class TestCourseCompletionModel(TestCase):
    """
    Tests for the CourseCompletin model:
    - shows the right text when a course is done/not done
    - 'completed' is False by default
    - each user can only have one record per course
    """
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(
            username='TestEszter',
            password='testpassword'
            )

        # create a test course
        self.course = Course.objects.create(
            title='Test Course',
            price=Decimal('24.99'),
            description='Description',
            content='Some content'
        )

    def test_str_output_completed(self):
        # test the __strs__ when course is marked completed
        completion = CourseCompletion.objects.create(
            user=self.user,
            course=self.course,
            completed=True
            )
        expected = f"{self.user.username} - {self.course.title} - Completed"
        self.assertEqual(str(completion), expected)

    def test_str_output_not_completed(self):
        # test the __strs__ when course is not completed (default)
        completion = CourseCompletion.objects.create(
            user=self.user,
            course=self.course
            )
        expected = (
            f"{self.user.username} - {self.course.title} - Not Completed"
            )
        self.assertEqual(str(completion), expected)

    def test_default_completed_false(self):
        # test that the default value for 'completed' is false
        completion = CourseCompletion.objects.create(
            user=self.user,
            course=self.course
            )
        self.assertFalse(completion.completed)

    def test_prevent_duplicate(self):
        # create the first course completion
        CourseCompletion.objects.create(
            user=self.user,
            course=self.course
            )
        # attempt to create a duplicate should raise an error
        with self.assertRaises(Exception):
            CourseCompletion.objects.create(
                user=self.user,
                course=self.course
                )


class ProfileViewsTest(TestCase):
    """
    Test the profile app views:
    - 'my_courses' returns the user's purchased courses
    - 'toggle_completion' toggles course completion status
    """

    def setUp(self):
        # create a test user and log them in
        self.user = User.objects.create_user(
            username='TestEszter',
            password='testpassword'
            )
        self.client.login(
            username='TestEszter',
            password='testpassword'
            )

        # create a test course
        self.course = Course.objects.create(
            title="Test Course",
            price=Decimal("12.95"),
            description="description",
            content="Some Content"
        )

        # create a test purchase for the user
        self.purchase = Purchase.objects.create(
            user=self.user,
            email='test@test.com',
            full_name='Test Eszter',
            street_address1='19 Test Street',
            city='Test City',
            postcode='424242',
            country='IE',
            access_granted=True
        )

        # add course to the purchase
        PurchaseItem.objects.create(
            purchase=self.purchase,
            course=self.course,
            quantity=1
        )

    def test_my_courses_view_status_code(self):
        # test if the view loads
        response = self.client.get(reverse('my_courses'))
        self.assertEqual(response.status_code, 200)

        # check is the correct template is used
        self.assertTemplateUsed(
            response,
            'profiles/my_courses.html'
            )

        # context should include the owned course
        self.assertIn('owned_courses', response.context)
        self.assertEqual(
            len(response.context['owned_courses']), 1
            )

    def test_toggle_completion_creates_and_updates(self):
        # make sure no CourseCompletion exits initially
        self.assertFalse(
            CourseCompletion.objects.filter(
                user=self.user, course=self.course).exists())

        # toggle to mark as completed
        response = self.client.post(
            reverse('toggle_completion', args=[self.course.id])
            )
        # should redirect to 'my_courses'
        self.assertRedirects(response, reverse('my_courses'))

        # completion record should now exist and be marked as completed
        completion = CourseCompletion.objects.get(
            user=self.user,
            course=self.course
            )
        self.assertTrue(completion.completed)

        # toggle again to mark as not completed
        self.client.post(reverse('toggle_completion', args=[self.course.id]))
        completion.refresh_from_db()
        self.assertFalse(completion.completed)
