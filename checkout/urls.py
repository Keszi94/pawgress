from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path(
        'checkout_success/<purchase_number>/',
        views.checkout_success, name='checkout_success'
        ),
    path('wh/', webhook, name='webhook'),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name='cache_checkout_data'
        ),
]
