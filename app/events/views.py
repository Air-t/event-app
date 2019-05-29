from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse_lazy

from .models import Event
from .forms import FeedbackForm, EventForm, EventSearchForm
from .mixins import LoginRequiredOwnerMixin


def goto(request):
    """Redirects client to the home page."""
    return redirect('events:events')


class EventsView(ListView):
    """Handles events list view"""
    model = Event
    template_name = 'events/client/events.html'

    def get_queryset(self):
        return Event.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventView(DeleteView):
    """Handles event detail view"""
    model = Event
    template_name = 'events/client/event.html'
    pk_url_kwarg = 'pk'

    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


# Info section
class FeedbackView(View):
    """Handles feedback view - sends user coment to app email mailbox."""
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
