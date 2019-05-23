from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Event


class FeedbackForm(forms.Form):
    """Form to handle users feedback"""
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 40,
                                                           'rows': 5,
                                                           'placeholder': 'Your comment.'}), required=True, label='')
    email = forms.EmailField(required=True, label='', help_text="Email field")


class EventForm(forms.ModelForm):
    """Form to create new Exam instance"""

    start_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input text-muted',
            'data-target': '#datetimepicker1',
            'width': '100px',
            'placeholder': 'Start date',
        })
    )

    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input text-muted',
            'data-target': '#datetimepicker1',
            'width': '100px',
            'placeholder': 'End date',
        })
    )

    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date']
        labels = {
            'name': '',
            'start_date': 'start date',
            'end_date': 'start date',

        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Event name goes here.'),
                                           'error_messages': _('This event already exists.'),
                                           }),
        }
