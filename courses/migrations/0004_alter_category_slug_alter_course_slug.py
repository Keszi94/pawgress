# Generated by Django 5.2 on 2025-05-01 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_category_slug_course_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
