from django.urls import path
from .views import EventListView, EventDetailView, EventCreateView
from . import views

urlpatterns = [
    path('', EventListView.as_view(), name='tracker-home'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/new/', EventCreateView.as_view(), name='event-create'),
]