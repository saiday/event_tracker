from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
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
    paginate_by = 10


class UserEventListView(ListView):
    """
    default template should be at: tracker/event_list.html
    """

    model = Event
    template_name = 'tracker/user_events.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Event.objects.filter(confirmed_user=user).order_by('-last_modified')


class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['is_one_of_confirmed_user'] = self.get_object().confirmed_user.filter(id=self.request.user.id).exists()
        return context


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
