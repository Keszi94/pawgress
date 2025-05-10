from django.contrib import admin
from .models import Purchase, PurchaseItem

# Register your models here.


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    readonly_fields = ('item_total',)
    extra = 0


# registers the model with the admin class
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = (
        'purchase_number',
        'date',
        'grand_total',
        'is_paid',
        'stripe_payment_intent'
        )

    fields = ('purchase_number',
              'user',
              'email',
              'date',
              'grand_total',
              'is_paid',
              'stripe_payment_intent'
              )

    list_display = ('purchase_number',
                    'user',
                    'date',
                    'grand_total',
                    'is_paid'
                    )

    ordering = ('-date',)
    inlines = (PurchaseItemInline,)
