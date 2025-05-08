from django.shortcuts import render
from .models import Bundle

# Create your views here.


def all_bundles(request):
    """ A view to show all the bundles"""

    bundles = Bundle.objects.all()

    context = {
        'bundles': bundles,
    }

    return render(request, 'bundles/bundles.html', context)
