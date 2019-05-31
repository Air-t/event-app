from django.urls import path

from .views import EventsView, EventsOwnerView, EventCreateView, EventDeleteView, EventSearchView, EventView
from .views import AddToCartView, CartView, CartDeleteItemView, EventOwnerView, SeatCreateView

app_name = 'events'

urlpatterns = [
    path('events/', EventsView.as_view(), name='events'),
    path('events/event/<int:pk>/', EventView.as_view(), name='event'),
    path('manage/event/<int:pk>/', EventOwnerView.as_view(), name='owner-event'),
    path('manage/events/', EventsOwnerView.as_view(), name='owner-events'),
    path('manage/events/create/', EventCreateView.as_view(), name='owner-event-create'),
    path('manage/event/<int:pk>/seat/create/', SeatCreateView.as_view(), name='owner-event-seat-create'),
    path('manage/events/delete/<int:pk>/', EventDeleteView.as_view(), name='owner-event-delete'),
    path('events/search/', EventSearchView.as_view(), name='events-search'),
    path('<str:username>/cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add-ticket'),
    path('cart/delete/<int:pk>/', CartDeleteItemView.as_view(), name='delete-ticket'),

]
