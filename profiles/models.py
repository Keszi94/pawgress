from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

"""
Profile app models:
- UserProfile: an extension of the built in Django User model
- CourseCompletion: Tracks which courses a user completed
  Useful for analytics
"""


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # displays the username
    def __str__(self):
        return self.user.usename


class CourseCompletion(models.Model):
    # The user who completd the course
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # the course being tracked
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # true if course is marked completed
    completed = models.BooleanField(default=False)

    class Meta:
        # prevents duplicates
        unique_together = ('user', 'course')

    def __str__(self):
        status = 'Completed' if self.completed else 'Not Completed'
        return f"{self.user.username} - {self.course.title} - {status}"
