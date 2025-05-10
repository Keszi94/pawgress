from .models import PurchaseItem
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=PurchaseItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update the purchase total when a PurchaseItem is added
    """
    instance.purchase.update_total()


@receiver(post_delete, sender=PurchaseItem)
def update_on_delet(sender, instance, **kwargs):
    """
    Update the purchase total when a PurchaseItem is deletred
    """
    instance.purchase.update_total()
