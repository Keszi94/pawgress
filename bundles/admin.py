from django.contrib import admin
from .models import Bundle

# Register your models here.


class BundleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'get_courses_count',
        'created_at'
    )

    ordering = (
        'title',
        )

    search_fields = (
        'title',
        'description'
    )

    filter_horizontal = (
        'courses',
    )

    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Bundle, BundleAdmin)
