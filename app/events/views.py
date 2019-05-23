from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy

from .models import Event
from .forms import FeedbackForm, EventForm
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


class EventOwnerView(LoginRequiredOwnerMixin, UserPassesTestMixin, ListView):
    """Handles events list view"""
    model = Event
    template_name = 'events/owner/owner_event.html'

    def get_queryset(self):
        return Event.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventForm()
        return context


class ExamCreateView(LoginRequiredOwnerMixin, UserPassesTestMixin, CreateView):
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


# Info section

class FeedbackView(View):
    def get(self, request):
        return render(request, 'events/info/leave_feedback.html', {'form': FeedbackForm()})

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('email'))
            try:
                send_mail('Exam App feedback',
                          f"{form.cleaned_data.get('comment')}",
                          f"{form.cleaned_data.get('email')}",
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
