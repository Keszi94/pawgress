from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_courses, name='courses'),
    path('<course_id>', views.course_detail, name='course_detail'),
    path('admin/create/', views.course_create, name='course_create'),
    path(
        'admin/delete/<int:course_id>',
        views.course_delete,
        name='course_delete'
        )
]
