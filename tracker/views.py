from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['key', 'value', 'description']

    def form_valid(self, form):
        form.save()
        instance = form.instance
        instance.confirmed_user.add(self.request.user)
        instance.save()
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if event.confirmed_user.filter(id=self.request.user.id).exists():
            return True
        return False


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('tracker-home')

    def test_func(self):
        event = self.get_object()
        if event.confirmed_user.filter(id=self.request.user.id).exists():
            return True
        return False
