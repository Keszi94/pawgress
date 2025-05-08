from django.contrib import admin
from .models import Course, Category

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'price',
        'image'
    )

    ordering = ('title', )

    search_fields = (
        'title',
        'description'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'pk'
    )


admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
