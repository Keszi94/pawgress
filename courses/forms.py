from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'description',
            'content', 'price', 'category',
            'image', 'time_frame'
            ]
        # Give exta space for title and description
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': (
                        'form-control form-control-lg '
                        'border border-1 border-black'
                        )}),
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'form-control border border-1 border-black'
                    }),
            'content': CKEditorWidget(),
        }
