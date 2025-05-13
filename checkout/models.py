import uuid

from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from bundles.models import Bundle
from django.db.models import Sum

# Create your models here.


# Represents a simple completed purchase
class Purchase(models.Model):
    purchase_number = models.CharField(
        max_length=32, null=False,
        editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True)
    email = models.EmailField(max_length=254, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    # billing fields
    full_name = models.CharField(max_length=80, null=False, blank=True)
    # Optional bussiness info
    company_name = models.CharField(max_length=100, blank=True, null=True)
    street_address1 = models.CharField(max_length=80, null=False, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=40, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)

    # Payment data
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=False, default=0.00)
    is_paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(
        max_length=255, blank=True, null=True)
    original_cart = models.TextField(null=False, blank=False, default='')

    # Course access
    access_granted = models.BooleanField(default=False)

    # auto-generates a random order number
    def _generate_purchase_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.purchase_number:
            self.purchase_number = self._generate_purchase_number()
        super().save(*args, **kwargs)

    # calculates the total
    def update_total(self):
        total = self.items.aggregate(Sum('item_total'))['item_total__sum'] or 0
        self.grand_total = total
        self.save()

    def __str__(self):
        return f'Purchase {self.purchase_number}'


# Represents an item in the purchase (course or bundle)
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE,
        related_name='items')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True)
    bundle = models.ForeignKey(
        Bundle, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    item_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False,
        blank=False, editable=False)

    def save(self, *args, **kwargs):
        # calculates the total before saving
        if self.course:
            self.item_total = self.course.price * self.quantity
        elif self.bundle:
            self.item_total = self.bundle.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        if self.course:
            return f'{self.course.title} (x{self.quantity})'
        elif self.bundle:
            return f'{self.bundle.title} (x{self.quantity})'
        return "Unknown Item"
