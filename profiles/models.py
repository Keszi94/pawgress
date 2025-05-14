from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CourseCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        status = 'Completed' if self.completed else 'Not Completed'
        return f"{self.user.username} - {self.course.title} - {status}"
