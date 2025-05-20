from django.db import models
from courses.models import Course
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

"""
Bundles app models:
- Bundle: A collection of related courses offered
  together at a discounted price.
  Supports automatic price aggregation,
  savings calculaation and course management.
"""


class Bundle(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=100,
        # stop admins from filling out slug field
        help_text="Leave blank, autogenerates from the title."
        )
    description = models.TextField()
    # one bundle can have many courses in it and
    # one course can be in many bundles
    courses = models.ManyToManyField(Course, related_name='bundles')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # added two seperate folders for course and bundle images for neatness
    image = CloudinaryField(
        folder='bundle_images', blank=True, null=True
        )
    # helps keeping site content up to date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # Auto calculate values for prices
    total_value = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00, editable=False
        )
    savings = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_courses_count(self):
        # amount of courses in the bundle
        return self.courses.count()

    def __str__(self):
        return self.title
