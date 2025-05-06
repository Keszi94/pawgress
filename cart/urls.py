from django.urls import path
from . import views

urlpatterns = [
    # shows the cart page
    path('', views.view_cart, name='view_cart'),
    # adds course to the cart
    path('add<item_id>/', views.add_to_cart, name='add_to_cart'),
]