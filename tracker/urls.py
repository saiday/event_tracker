from django.urls import path
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView
from . import views

urlpatterns = [
    path('', EventListView.as_view(), name='tracker-home'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/new/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/update', EventUpdateView.as_view(), name='event-update'),
]
