from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from checkout.models import Purchase
from profiles.models import CourseCompletion
from courses.models import Course

# Create your views here.


@login_required
def my_courses(request):
    # Get all purchases for the logged-in user

    purchases = Purchase.objects.filter(
        user=request.user, access_granted=True
        )

    owned_courses = set()

    for purchase in purchases:
        for item in purchase.items.all():
            if item.course:
                owned_courses.add(item.course)
            elif item.bundle:
                for course in item.bundle.courses.all():
                    owned_courses.add(course)

    courses_with_completion = []

    # Go through each owned course
    for course in owned_courses:
        # Try to find completion record for this course
        try:
            completion = CourseCompletion.objects.get(
                user=request.user, course=course
                )
            # If completed, mark the course as completed
            course.completed = completion.completed
        except CourseCompletion.DoesNotExist:
            # If not indicated completed, default to not completed
            course.completed = False

        # Add this course to the final list
        courses_with_completion.append(course)

    return render(request, 'profiles/my_courses.html', {
        'owned_courses': courses_with_completion
    })


@require_POST
@login_required
def toggle_completion(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    completion, created = CourseCompletion.objects.get_or_create(
        user=request.user,
        course=course
    )
    completion.completed = not completion.completed
    completion.save()
    return redirect('my_courses')
