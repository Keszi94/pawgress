from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# Generates a search query
from django.db.models import Q
from .models import Course, Category

# Create your views here.


def all_courses(request):
    """A view to show all the courses, with search and filtering"""

    courses = Course.objects.all()
    categories = Category.objects.all()
    query = None
    current_category = None

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        courses = courses.filter(category=current_category)

    # Searchbar handling
    if 'q' in request.GET:
        # space-only " " search is also invalid (.strip())
        query = request.GET['q'].strip()
        if not query:
            messages.error(
                request,
                "Please type a course name or keyword to start searching."
                )
            # Bug fix: return to the same page,
            # not the courses page, when field is empty
            return redirect(
                request.META.get('HTTP_REFERER',
                                 reverse('courses')
                                 ))

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
        'categories': categories,
        'current_category': current_category,
        'search_term': query,
    }

    return render(request, 'courses/courses.html', context)


def course_detail(request, course_id):
    """A view to show the content of a specific course - if purchased"""

    course = get_object_or_404(Course, pk=course_id)

    context = {
        'course': course,
    }

    return render(request, 'courses/course_detail.html', context)
