from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# Generates a search query
from django.db.models import Q

from .forms import CourseForm
from checkout.models import Purchase
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

    # Default to false
    has_access = False

    if request.user.is_authenticated:
        # Get all confirmed purchases from the user
        purchases = Purchase.objects.filter(
            user=request.user,
            access_granted=True
            )
        # Loop through each purchase and the items in them
        for purchase in purchases:
            for item in purchase.items.all():
                if item.course == course:
                    has_access = True
                elif item.bundle:
                    if course in item.bundle.courses.all():
                        has_access = True

    context = {
        'course': course,
        'has_access': has_access
    }

    return render(request, 'courses/course_detail.html', context)


def course_create(request):
    """
    A view to allow superusers to create a new course on the fornt-end
    """
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(
            request,
            "You do not have permission to access this page."
            )
        return redirect('home')

    form = CourseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Course created successfully!")
        return redirect('courses')

    return render(request, 'courses/course_form.html', {
        'form': form,
        'form_title': 'Add New Course'
        })


def course_delete(request, course_id):
    """
    A view that allows superusers to delete a course from the front-end
    """
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(
            request,
            "Only site admins are allowed to perform this action!"
        )
        return redirect('home')

    course = get_object_or_404(Course, pk=course_id)
    title = course.title
    course.delete()
    messages.success(
        request,
        f'Course "{title}" has been deleted successfully!'
        )
    return redirect('courses')


def course_edit(request, course_id):
    """
    A view that allows superusers to eit an existing course
    """
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(
            request,
            "Only site admins are allowed to access this page!"
            )
        return redirect('home')

    course = get_object_or_404(Course, pk=course_id)
    form = CourseForm(
        request.POST or None,
        request.FILES or None,
        instance=course
        )

    if form.is_valid():
        form.save()
        messages.success(
            request,
            f'Course "{course.title}" has been updated successfully!'
        )
        return redirect('courses')

    return render(request, 'courses/course_form.html', {
        'form': form,
        'form_title': f'Edit Course: {course.title}',
    })
