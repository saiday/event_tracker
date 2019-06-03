from django.shortcuts import render

from tracker.models import Event


def home(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'tracker/home.html', context)
