from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_courses, name='courses'),
    path('<course_id>', views.course_detail, name='course_detail'),
]
