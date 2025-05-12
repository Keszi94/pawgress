from django.db import models
from courses.models import Course
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from decimal import Decimal, ROUND_HALF_UP

# Create your models here.


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
    image = models.ImageField(
        upload_to='bundle_images/', blank=True, null=True
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

        # Recalculate the values before saving
        course_prices = (
            self.courses.aggregate(total=models.Sum('price'))['total'] or 0.00
            )
        self.total_value = course_prices
        self.savings = (
            course_prices - self.price
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        super().save(*args, **kwargs)

    def get_courses_count(self):
        # amount of courses in the bundle
        return self.courses.count()

    def __str__(self):
        return self.title


# Signal for automatically updating the total value and
# savings for a bundle
@receiver(m2m_changed, sender=Bundle.courses.through)
def update_bundle_totals(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        course_prices = (
            instance.courses.aggregate(
                total=models.Sum('price'))['total'] or 0.00
            )
        instance.total_value = course_prices
        instance.savings = (course_prices - instance.price).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        # Avoid triggering the signal again
        Bundle.objects.filter(pk=instance.pk).update(
            total_value=instance.total_value,
            savings=instance.savings
        )
