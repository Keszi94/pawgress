from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Bundle
from decimal import Decimal, ROUND_HALF_UP
from django.db import models


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
