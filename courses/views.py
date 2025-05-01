from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# Generates a search query
from django.db.models import Q
from .models import Course

# Create your views here.


def all_courses(request):
    """A view to show all the courses"""

    courses = Course.objects.all()

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request,
                    "Please type a course name or keyword to start searching."
                    )
                return redirect(reverse('courses'))

            # either the title or the description contains the query
            # icontains = case-INsensitive substring match
            queries = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(content__icontains=query)
            )
            courses = courses.filter(queries)

    context = {
        'courses': courses,
        'search_term': query
    }

    return render(request, 'courses/courses.html', context)


def course_detail(request, course_id):
    """A view to show the content of a specific course - if purchased"""

    course = get_object_or_404(Course, pk=course_id)

    context = {
        'course': course,
    }

    return render(request, 'courses/course_detail.html', context)
