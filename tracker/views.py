from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from tracker.models import Event


def home(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'tracker/home.html', context)


class EventListView(ListView):
    """
    default template should be at: tracker/event_list.html
    """

    model = Event
    template_name = 'tracker/home.html'
    context_object_name = 'events'
    ordering = ['-last_modified']


class EventDetailView(DetailView):
    model = Event


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['key', 'value', 'description']
    success_url = reverse_lazy('tracker-home')

    def form_valid(self, form):
        form.save()
        instance = form.instance
        instance.confirmed_user.add(self.request.user)
        instance.save()
        return super().form_valid(form)
