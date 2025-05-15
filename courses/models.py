from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

"""
Courses app models:
- Category: Defines categories for the courses.
- Course: Represents individual training courses with pricing,
  content, and duration.
  Supports categorization, estimated completion time, and descreiptions.
"""


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    DURATION_CHOICES = [
        ('1w', '1 Week'),
        ('2w', '2 Weeks'),
        ('3w', '3 Weeks'),
        ('1m', '1 Month'),
        ('2m', '2 Months'),
        ('3m', '3 Months'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=100,
        # stop admins from filling out slug field
        help_text="Leave blank, autogenerates from the title."
        )
    description = models.TextField(max_length=300)
    content = RichTextField()  # ck editor
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='courses'
        )
    # added two seperate folders for course and bundle images for neatness
    image = models.ImageField(
        upload_to='course_images/', blank=True, null=True
        )
    # helps keeping site content up to date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # time frame - how long it takes to implement changes with dogs
    time_frame = models.CharField(
        max_length=2, choices=DURATION_CHOICES,
        default='2w',
        help_text="Estimated time to complete"
        " the course with consistent practice"
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
