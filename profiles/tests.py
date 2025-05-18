from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal

from courses.models import Course
from profiles.models import CourseCompletion

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
