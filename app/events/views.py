from datetime import datetime, timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse_lazy
from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models import Sum, Count

from .models import Event, EventSeat, EventTicket, TicketReservation
from .forms import FeedbackForm, EventForm, EventSearchForm, BookTicketForm, EventSeatForm
from .mixins import LoginRequiredOwnerMixin

User = get_user_model()


@receiver(request_finished)
def remove_unpayed_tickets(sender, **kwargs):
    """Removes all unpayed tickets and ticket reservation models based on date expire"""
    # TODO use sheduler instead sigman triggered in request_finished
    tickets = EventTicket.objects.all().filter(is_payed=False).filter(is_in_payment=False)
    [ticket.delete() for ticket in tickets if ticket.ticketreservation.date_expired < datetime.now(timezone.utc)]


def goto(request):
    """Redirects client to the home page."""
    return redirect('events:events')


class EventsView(ListView):
    """Handles events list view"""
    model = Event
    template_name = 'events/client/events.html'

    def get_queryset(self):
        return Event.objects.all().order_by('name')


class EventView(DetailView):
    """Handles event detail view"""
    model = Event
    template_name = 'events/client/event.html'
    pk_url_kwarg = 'pk'

    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookTicketForm()
        return context


class EventsOwnerView(LoginRequiredOwnerMixin, UserPassesTestMixin, ListView):
    """Handles events list view"""
    model = Event
    template_name = 'events/owner/owner_event.html'

    def get_queryset(self):
        return Event.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventForm()
        return context


class EventOwnerView(LoginRequiredOwnerMixin, UserPassesTestMixin, DetailView):
    """Handles event detail view"""
    model = Event
    template_name = 'events/owner/owner_event_seat.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventSeatForm()
        return context


class SeatCreateView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """Handles seat create view"""

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = EventSeatForm(data=request.POST)
        if form.is_valid():
            try:
                seat = form.save(commit=False)
                seat.event = event
                seat.save()
                messages.success(request, f"You have created new seat")
            except Exception as e:
                messages.warning(request, f"This type of tickets already exists.")
        else:
            messages.warning(self.request, "An error has occurred. Seat not created.")
        return redirect('events:owner-event', pk=pk)


class EventCreateView(LoginRequiredOwnerMixin, UserPassesTestMixin, CreateView):
    """Handles event create view"""
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('events:owner-events')

    def form_valid(self, form):
        event = form.save()
        messages.success(self.request, f"You have created new event - {event.name.lower()}")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "An error has occurred. Event not created.")
        return redirect('events:owner-events')


class EventSearchView(View):
    """Handles search event view"""

    def get(self, request):
        return render(request, 'events/event_search.html', {'form': EventSearchForm()})

    def post(self, request):
        form = EventSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            city = form.cleaned_data.get('city')
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')

            # cache enable
            if cache.get('event_list') is not None:
                events = cache.get('event_list')
            else:
                events = Event.objects.all().order_by('name')

            if name:
                events = events.filter(name__icontains=name)

            if city:
                events = events.filter(city__icontains=city)

            if to_date or from_date:
                if from_date and to_date:
                    events = events.filter(start_date__gte=from_date).filter(end_date__lte=to_date)
                elif from_date:
                    events = events.filter(start_date__gte=from_date)
                else:
                    events = events.filter(end_date__lte=to_date)

            if events.count() == 0:
                messages.info(request, "Sorry, we have no movies matching your criteria. Try once again.")
            else:
                cache.set('events_list', events)

            return render(request, 'events/event_search.html', {'object_list': events, 'form': form})

        messages.info(request, 'Please check your form input')
        return render(request, 'events/event_search.html', {'form': form})


class EventDeleteView(LoginRequiredOwnerMixin, UserPassesTestMixin, DeleteView):
    """Handles event delete view"""
    model = Event
    success_url = reverse_lazy('events:owner-events')
    pk_url_kwarg = 'pk'


class AddToCartView(LoginRequiredMixin, View):
    """Handles add to cart view"""

    def post(self, request, pk):
        seat = get_object_or_404(EventSeat, pk=pk)
        form = BookTicketForm(data=request.POST)
        event_id = int(request.POST.get('event_id'))
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            if quantity <= seat.tickets_available:
                for i in range(quantity):
                    try:
                        ticket = EventTicket.objects.create(seat=seat, user=request.user)
                        ticket.save()
                        reservation = TicketReservation.objects.create(ticket=ticket)
                        reservation.save()
                    except Exception as e:
                        print(e)
                        messages.warning(request, "Could not book tickets. Please try again later.")
            else:
                messages.warning(request, "Insufficient ticket quantity.")
        return redirect('events:event', pk=event_id)


class CartView(LoginRequiredMixin, View):
    """Handles cart view"""

    def get(self, request, username):
        user = get_object_or_404(User, pk=request.user.id)
        summary = user.eventticket_set.aggregate(Count('seat__price'), Sum('seat__price'))
        user_tickets = EventTicket.objects.all().filter(user=user)
        user_summary_by_ticket_event = user_tickets.distinct('seat__event__name')
        user_summary_by_ticket_type = user_tickets.distinct('seat__type')
        return render(request, 'events/client/cart.html', {'object': user.eventticket_set.all().order_by('seat__type'),
                                                           'summary': summary,
                                                           'events': user_summary_by_ticket_event,
                                                           'types': user_summary_by_ticket_type})

    def post(self, request, username):
        user = get_object_or_404(User, pk=request.user.id)
        return render(request, 'events/client/cart.html')


class CartDeleteItemView(LoginRequiredMixin, View):
    """Handles ticket/reservation delete view"""

    def post(self, request, pk):
        ticket = get_object_or_404(EventTicket, pk=pk)
        ticket.delete()
        return redirect('events:cart', username=request.user.username)


# Info section
class FeedbackView(View):
    """Handles feedback view - sends user comment to app email mailbox."""

    def get(self, request):
        return render(request, 'events/info/leave_feedback.html', {'form': FeedbackForm()})

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('email'))
            try:
                send_mail('Event app feedback',
                          f"{form.cleaned_data.get('comment')}\n",
                          f"sender: {form.cleaned_data.get('email')}\n",
                          [settings.DEFAULT_FROM_EMAIL],
                          fail_silently=False,
                          )
            except Exception as e:
                messages.warning(request, 'Fail to leave feedback.')
                return render(request, 'events/info/leave_feedback.html', {'form': FeedbackForm()})

            messages.success(request, 'Thanks for your comment!')
            return redirect('events:events')
        else:
            messages.warning(request, 'Fail to leave feedback.')
            return render(request, 'events/info/leave_feedback.html', {'form': FeedbackForm()})
