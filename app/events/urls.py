from django.urls import path

from .views import EventsView, EventOwnerView, EventCreateView, EventDeleteView, EventSearchView


app_name = 'events'


urlpatterns = [
    path('events/', EventsView.as_view(), name='events'),
    path('manage/events/', EventOwnerView.as_view(), name='owner-events'),
    path('manage/events/create/', EventCreateView.as_view(), name='owner-event-create'),
    path('manage/events/delete/<int:pk>/', EventDeleteView.as_view(), name='owner-event-delete'),
    path('events/search/', EventSearchView.as_view(), name='events-search'),

]