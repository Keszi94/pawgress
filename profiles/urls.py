from django.urls import path
from . import views

urlpatterns = [
    path('my_courses/', views.my_courses, name='my_courses'),
    path(
        'toggle_completion/<int:course_id>/',
        views.toggle_completion,
        name='toggle_completion'
        ),
]
