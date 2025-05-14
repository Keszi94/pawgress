from django.contrib import admin
from .models import CourseCompletion

# Register your models here.


@admin.register(CourseCompletion)
class CourseCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'completed',)
    list_filter = ('completed',)
    search_fields = ('user__username', 'course__title')
