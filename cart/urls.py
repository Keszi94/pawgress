from django.urls import path
from . import views

urlpatterns = [
    # shows the cart page
    path('', views.view_cart, name='view_cart'),
    # adds course to the cart
    path('add<item_id>/', views.add_to_cart, name='add_to_cart'),
    # remove course from the cart
    path(
        'remove/<item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
        ),
]
