from django.urls import path

from .views import EventsView, EventOwnerView, ExamCreateView


app_name = 'events'


urlpatterns = [
    path('events/', EventsView.as_view(), name='events'),
    path('manage/events/', EventOwnerView.as_view(), name='owner-events'),
    path('manage/events/create/', ExamCreateView.as_view(), name='owner-event-create')
]