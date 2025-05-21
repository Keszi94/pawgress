from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Bundle


# Signal for automatically updating the total value and
# savings for a bundle
@receiver(m2m_changed, sender=Bundle.courses.through)
def update_bundle_totals(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.save()
